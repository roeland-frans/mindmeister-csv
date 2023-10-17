from setuptools import find_namespace_packages
from setuptools import setup

with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name="mm2csv",
    version="1.0.0",
    author="Roeland van Nieuwkerk",
    description=(
        "Converts a mindmap *.mind* file exported from MindMeister to a *.csv* "
        "file."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/roeland-frans/mindmeister-csv",
    packages=find_namespace_packages(),
    entry_points={"console_scripts": ["mm2csv = mm2csv.mm2csv:main"]},
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[],
)
