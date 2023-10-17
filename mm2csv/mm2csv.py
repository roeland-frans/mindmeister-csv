import argparse
import csv
import json
import logging
import os
import shutil
import sys
import tempfile
import uuid
import zipfile

from io import FileIO
from typing import Optional

logger = logging.getLogger("MindMeister")
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "%(name)s: %(asctime)s - %(levelname)s - %(message)s"
)
ch.setFormatter(formatter)

logger.addHandler(ch)


class ExtractorError(Exception):
    pass


class MindMeisterExtractor:
    """
    This class will extract a .mind file and convert it to a flat .csv file.
    """

    def __init__(
        self, print_numbers: bool, print_ids: bool, print_leaf_nodes: bool
    ):
        self.input_file: Optional[FileIO] = None
        self.output_file: Optional[FileIO] = None
        self.csv_writer: Optional[csv.writer] = None
        self.print_numbers: bool = print_numbers
        self.print_ids: bool = print_ids
        self.print_leaf_nodes: bool = print_leaf_nodes

    @staticmethod
    def generate_id():
        return str(uuid.uuid4())

    def init_csv_writer(self) -> csv.writer:
        return csv.writer(
            self.output_file,
            delimiter=",",
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL,
        )

    def parse(self, parent_id: str, depth: int, numbers: str, node: dict):
        """
        This is a recursive function that is used to walk the Mind Meister
        hierarchy and output the title with a number prefix.

        :param depth: The current depth in the hierarchy.
        :param numbers: The string of numbers for the current node
                        e.g. '1.2.4.5'.
        :param node: The node element currently processed, this is a dictionary.
        """
        id = self.generate_id()
        has_children = False

        if "children" in node and len(node["children"]) > 0:
            has_children = True

        if "title" in node:
            row = list()

            if self.print_numbers:
                row.append(numbers)
            if self.print_ids:
                row.append(".".join([parent_id, id]))
            if self.print_leaf_nodes:
                if not has_children:
                    row.append("L")
                else:
                    row.append("")

            title = node["title"]
            title = title.replace("\r", " ")
            row.append(title)
            self.csv_writer.writerow(row)

        if has_children:
            count = 1

            for child_node in node["children"]:
                self.parse(
                    parent_id=id,
                    depth=depth + 1,
                    numbers=f"{numbers}.{count}",
                    node=child_node,
                )
                count += 1

    def unzip(self, file_path: str) -> str:
        """
        This will unzip the given file into a temporary folder.

        :param file_path: The path of the file to extract.
        :returns: The path to the temporary folder that was extracted.
        """
        temp_dir = tempfile.gettempdir()
        dest_dir = os.path.join(temp_dir, "mindmeister")

        with zipfile.ZipFile(file_path) as zip_file:
            for member in zip_file.infolist():
                # Path traversal defense copied from
                # http://hg.python.org/cpython/file/tip/Lib/http/server.py#l789
                words = member.filename.split("/")
                path = dest_dir
                for word in words[:-1]:
                    drive, word = os.path.splitdrive(word)
                    head, word = os.path.split(word)
                    if word in (os.curdir, os.pardir, ""):
                        continue
                    path = os.path.join(path, word)
                zip_file.extract(member, path)

        return dest_dir

    def convert(self, input_file_path: str, output_file_path: str):
        """
        Opens and parses the input file and if the data is in the correct
        format it will produce a flat representation of the Mind Meister
        hierarchy.

        :param input_file_path: The file path of the .mind file to read from.
        :param output_file_path: The file path of the .csv file to write to,
                                 if this is an empty string it will print the
                                 result to stdout.
        :raises ExtractorError: An ExtractorError is raised with the data
                                format is incorrect.
        """

        mind_meister_dir = None

        try:
            mind_meister_dir = self.unzip(input_file_path)
            self.input_file = open(os.path.join(mind_meister_dir, "map.json"))

            if output_file_path != "":
                self.output_file = open(output_file_path, "w")
            else:
                self.output_file = sys.stdout

            self.csv_writer = self.init_csv_writer()

            try:
                data = json.load(self.input_file)
            except ValueError:
                raise ExtractorError(
                    "Could not load the MindMeister map file, is this a "
                    "correct .mind file?"
                )

            if "root" in data:
                self.parse(
                    parent_id=self.generate_id(),
                    depth=0,
                    numbers="1",
                    node=data["root"],
                )
            else:
                raise ExtractorError(
                    "Incorrect data format, is this a correct .mind file?"
                )

        except IOError as error:
            logger.error(f"File error: {error}")

        finally:
            if self.input_file:
                self.input_file.close()
            if self.output_file:
                self.output_file.close()
            if mind_meister_dir:
                shutil.rmtree(mind_meister_dir)


def main():
    args_parser = argparse.ArgumentParser(
        description=(
            "This extracts a Mind Meister .mind file and converts it to a "
            "flat .csv file."
        )
    )
    args_parser.add_argument(
        "file", help="The .mind file to convert.",
    )
    args_parser.add_argument(
        "--output",
        type=str,
        nargs=1,
        default=[""],
        help="The .csv file to save to.",
    )
    args_parser.add_argument(
        "--numbers",
        help="Print hierarchy numbers for each item e.g. 1.2.3 (False).",
        action="store_true",
    )
    args_parser.add_argument(
        "--ids",
        help=(
            "Generate parent child ids to retain hierarchy relationships "
            "(False)."
        ),
        action="store_true",
    )
    args_parser.add_argument(
        "--leaf",
        help="Mark leaf nodes with an 'L' (False).",
        action="store_true",
    )
    args = args_parser.parse_args()

    extractor = MindMeisterExtractor(
        print_numbers=args.numbers,
        print_ids=args.ids,
        print_leaf_nodes=args.leaf,
    )

    try:
        extractor.convert(
            input_file_path=args.file, output_file_path=args.output[0]
        )

    except ExtractorError as error:
        logger.error(error)


if __name__ == "__main__":
    main()
