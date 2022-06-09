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
    fieldnames = ['CROP_NAME','DOC_NAME','URL','CHUNK','CVAR_DATA_SOURCE_ID','CVAR','NER_TAG_LABEL','CROP_ATTRIBUTE_VALUE']

    # Create a file to contain the CSV file
    output_file = open(outputFileName, 'w')
    writer = csv.DictWriter(output_file, delimiter=',', fieldnames=fieldnames)
    writer.writeheader()

    # Iterate through each file
    for fileName in filePaths:
        # Convert it to mixed_type (see json2py.py for details on mixed_type)
        data = json_2_dict(fileName)
        doc_value = data['doc']
        url_value = data['url']
        chunk = data['chunk']
        crop=data['crop']
        cvar=data['cvar']

        # To try and save space, we are going to create an integer ID that should be
        # unique to each document, chunk and crop variety set using the hash
        # function
        id_str = doc_value + ":" + chunk + ":" + cvar
        id_value = hash(id_str)
        mixed_data = dict_2_mixed_type(data)

        # Extract each entry with annotated NER tags
        for entry in mixed_data:
            text_data = entry[0]
            ents = entry[1]['entities']

            # This loops goes through the entities and writes them out into a CSV file.
            for (start, end, ner_tag) in ents:
                if(ner_tag != 'CROP' and ner_tag != 'CVAR'):
                    writer.writerow({'CROP_NAME':crop, 'DOC_NAME':doc_value, 'URL':url_value,'CHUNK':chunk,'CVAR_DATA_SOURCE_ID':id_value, 'CVAR':cvar, 'NER_TAG_LABEL':ner_tag, 'CROP_ATTRIBUTE_VALUE':text_data[start:end].lower()})
                    
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
    # Example: python3 $path_to_src/json2csv.py subdir1 temp.csv
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
