#!/bin/env python3

import csv
from json2py import *

def convertJsonToCSV(outputFileName=None, filePaths=None):
    """
    :param outputFileName: Add documentation
    :param filePaths:
    :return:
    """

    # Header
    fieldnames = ['CROP','CVAR','ALAS', 'PATH', 'PLAN', 'TRAT', 'PPTD', 'PED', 'JRNL']


    # Create a file to contain the CSV file
    output_file = open(outputFileName, 'w')
    writer = csv.DictWriter(output_file, delimiter=',', fieldnames=fieldnames)
    writer.writeheader()

    # Iterate through each file
    for fileName in filePaths:
        # Convert it to mixed_type (see json2py.py for details on mixed_type)
        data = json_2_dict(fileName)
        mixed_data = dict_2_mixed_type(data)

        # Extract each entry with annotated NER tags
        for entry in mixed_data:
            print(entry)
            break
        break

    output_file.close()


def rawJsonToCSV(dir=None, outputFileName=None, suffix=".json", filename_substring="_cvar_"):
    """Add docstring"""

    # Walk through the directory and retrieve all files ending in fileSuffix
    path = os.walk(dir)
    filePaths = []
    for root, directories, files in path:
        # Scan files
        for name in files:
            if name.endswith(suffix) and filename_substring in name:
                filePaths.append(os.path.join(root, name))
        # Scan subdirectories
        for name in directories:
            if name.endswith(suffix) and filename_substring in name:
                filePaths.append(os.path.join(root, name))

    convertJsonToCSV(outputFileName,filePaths)




if __name__ == "__main__":

    #
    # Parse out the arguments and assign them to variables
    #
    parser = argparse.ArgumentParser(
        description="convert raw JSON to csv file that can be loaded into a database ",
        epilog="Example: python3 json2csv.py jsonFolder outputFileName (optional --suffix '.json' ; --filename_substring '_cvar_' "
    )
    parser.add_argument(
        'jsonFolder', help='Folder containing json files'
    )
    parser.add_argument(
        'outputFileName', help='Output Filename'
    )
    parser.add_argument(
        '--suffix', default=".json", type=str, help='Suffix the files ends in. Default=".json" '
    )
    parser.add_argument(
        '--filename_substring',
        help='Substring to look for in filename to identify qualifying files. Default = "_cvar_" '
    )

    if len(sys.argv) < 3:
        parser.print_usage()
        sys.exit()

    args = parser.parse_args()

    if args.suffix is None:
        args.suffix = ".json"
    if args.filename_substring is None:
        args.filename_substring = "_cvar_"

    rawJsonToCSV(dir=args.jsonFolder,outputFileName=args.outputFileName,suffix=args.suffix, filename_substring=args.filename_substring)
