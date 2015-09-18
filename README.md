# MindMeister

MindMeister is collaborative mind mapping software that allows its users to visualize their thoughts in the cloud.
It allows users to collaborate on mind maps using their desktop browsers or mobile applications - [MindMeister](https://www.mindmeister.com/).

Although MindMeister has a number of export options available it does not have an option to export to a .csv file.
Exporting to .csv particularly useful when you would like to import the hierarchy into Excel or Calc for further
analysis e.g. adding time estimates to work break down structures on a project.

# The Script

This is a simple Python script that will convert a *.mind* file into a *.csv* file.

## Requirements

- Python 2.7

## Usage

First export the mind map to a MindMeister *.mind* file. Once downloaded you can run the following commands.

```
./mm2csv.py --numbers --output mindmap.csv mindmap.mind
```

If you do not specify an output file with th *--output* option the script will print the csv output to stdout.
This is useful if you would like to pipe the output to other commands.

```
./mm2csv.py --numbers mindmap.mind | grep "Some search string"
```

## Options

**--output**: The .csv file to save to.

**--numbers**: Print hierarchy number for each item e.g. 1.2.3

**--ids**: Generage parent child ids to retain hierarchy relationships.

**--leaf**: Mark leaf nodes with an 'L'.