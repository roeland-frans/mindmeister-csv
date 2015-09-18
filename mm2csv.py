#!/usr/bin/env python
import argparse
import csv
import json
import logging
import os
import tempfile
import zipfile
import shutil
import uuid

logger = logging.getLogger('MindMeister')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(name)s: %(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

logger.addHandler(ch)

class ExtractorError(Exception):
    """
    This represents a general extractor error.
    """
    pass


class MindMeisterExtractor:
    """
    This class will extract a .mind file and convert it to a flat .csv file.
    """

    def __init__(self, print_numbers, print_ids, print_leaf_nodes):
        self.input_file = None
        self.output_file = None
        self.csv_writer = None
        self.print_numbers = print_numbers
        self.print_ids = print_ids
        self.print_leaf_nodes = print_leaf_nodes

    @staticmethod
    def generate_id():
        return str(uuid.uuid4())

    def parse(self, parent_id, depth, numbers, node):
        """
        This is a recursive function that is used to walk the Mind Meister hierarchy and output the
        title with a number prefix.

        :param depth: The current depth in the hierarchy.
        :param numbers: The string of numbers for the current node e.g. '1.2.4.5'.
        :param node: The node element currently processed, this is a dictionary.
        """
        id = self.generate_id()
        has_children = False


        if 'children' in node and len(node['children']) > 0:
            has_children = True

        if 'title' in node:
            if self.csv_writer:
                row = list()

                if self.print_numbers:
                    row.append(numbers)
                if self.print_ids:
                    row.append(id)
                    row.append(parent_id)
                if self.print_leaf_nodes:
                    if not has_children:
                        row.append('L')
                    else:
                        row.append('')

                row.append(node['title'])

                self.csv_writer.writerow(row)
            else:
                row = ''

                if self.print_numbers:
                    row += '{0},'.format(numbers)
                if self.print_ids:
                    row += '{0},{1},'.format(id, parent_id)
                if self.print_leaf_nodes:
                    if not has_children:
                        row += 'L,'
                    else:
                        row += ','

                row += node['title']

                print row

        if has_children:
            count = 1

            for child_node in node['children']:
                self.parse(id, depth + 1, numbers + '.{0}'.format(count), child_node)
                count += 1

    def unzip(self, file_path):
        """
        This will unzip the given file into a temporary folder.

        :param file_path: The path of the file to extract.
        :returns: The path to the temporary folder that was extracted.
        """
        temp_dir = tempfile.gettempdir()
        dest_dir = os.path.join(temp_dir, 'mindmeister')

        with zipfile.ZipFile(file_path) as zip_file:
            for member in zip_file.infolist():
                # Path traversal defense copied from
                # http://hg.python.org/cpython/file/tip/Lib/http/server.py#l789
                words = member.filename.split('/')
                path = dest_dir
                for word in words[:-1]:
                    drive, word = os.path.splitdrive(word)
                    head, word = os.path.split(word)
                    if word in (os.curdir, os.pardir, ''): continue
                    path = os.path.join(path, word)
                zip_file.extract(member, path)

        return dest_dir

    def convert(self, input_file_path, output_file_path):
        """
        Opens and parses the input file and if the data is in the correct format it will
        produce a flat representation of the Mind Meister hierarchy.

        :param input_file_path: The file path of the .mind file to read from.
        :param output_file_path: The file path of the .csv file to write to, if this is an empty string 
                                 it will print the result to stdout.
        :raises ExtractorError: An ExtractorError is raised with the data format is incorrect.
        """
        mind_meister_dir = self.unzip(input_file_path)

        try:
            self.input_file = open(os.path.join(mind_meister_dir, 'map.json'))
        except IOError, e:
            logger.error("File error: {0}".format(e))
            shutil.rmtree(mind_meister_dir)
            return

        if output_file_path != '':
            self.output_file = open(output_file_path, 'wb')
            self.csv_writer = csv.writer(
                self.output_file,
                delimiter=',',
                quotechar='"',
                quoting=csv.QUOTE_MINIMAL
            )

        try:
            data = json.load(self.input_file)
        except ValueError, e:
            raise ExtractorError("Could not load the MindMeister map file, is this a correct .mind file?")

        if 'root' in data:
            self.parse(self.generate_id(), 0, '1', data['root'])
        else:
            raise ExtractorError("Incorrect data format, is this a correct .mind file?")

        # Close file descriptors and remove temporary files
        self.input_file.close()
        if self.output_file:
            self.output_file.close()

        shutil.rmtree(mind_meister_dir)


if __name__ == '__main__':
    # Setup arguments
    args_parser = argparse.ArgumentParser(
        description='This extracts a Mind Meister .mind file and converts it to a flat .csv file.'
    )
    args_parser.add_argument(
        'file',
        help="The .mind file to convert.",
    )
    args_parser.add_argument(
        '--output',
        type=str,
        nargs=1,
        default=[''],
        help="The .csv file to save to.",
    )
    args_parser.add_argument(
        '--numbers',
        help="Print hierarchy numbers for each item e.g. 1.2.3 (False).",
        action='store_true'
    )
    args_parser.add_argument(
        '--ids',
        help="Generate parent child ids to retain hierarchy relationships (False).",
        action='store_true'
    )
    args_parser.add_argument(
        '--leaf',
        help="Mark leaf nodes with an 'L' (False).",
        action='store_true'
    )
    args = args_parser.parse_args()

    extractor = MindMeisterExtractor(
        print_numbers=args.numbers,
        print_ids=args.ids,
        print_leaf_nodes=args.leaf
    )

    try:
        extractor.convert(
            input_file_path=args.file,
            output_file_path=args.output[0]
        )

    except IOError, e:
        logger.error("File error: {0}".format(e))

    except ExtractorError, e:
        logger.error(e)
