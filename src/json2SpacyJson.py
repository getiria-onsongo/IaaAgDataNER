#!/bin/env python3
import spacy

from json2py import *
from sklearn.model_selection import train_test_split
from spacy.training import offsets_to_biluo_tags
from spacy.training import docs_to_json

def convertJsonToSpacyJsonl(model="en_core_web_lg",outputFileName=None, filePaths=None):
    # Load spacy pipeline
    nlp = spacy.load(model)
    # Create a file to contain the jsonl format for SpaCy
    file = open(outputFileName, "w")
    file.write("[")
    cnt = 0

    # Iterate through each file
    for fileName in filePaths:
        print("Working on file:", fileName)
        # Convert it to mixed_type (see json2py.py for details on mixed_type)
        data = json_2_dict(fileName)
        mixed_data = dict_2_mixed_type(data)

        # Extract each entry with annotated NER tags
        for entry in mixed_data:
            rawText = entry[0]
            doc = nlp(rawText)
            entities = entry[1]['entities']
            tags = offsets_to_biluo_tags(doc, entities)
            docs_dict = docs_to_json([doc], cnt)
            for i in range(len(docs_dict['paragraphs'][0]['sentences'][0]['tokens'])):
                docs_dict['paragraphs'][0]['sentences'][0]['tokens'][i]['ner'] = tags[i]
            if (cnt > 0):
                file.write(",")
                file.write("\n")
            file.write(json.dumps(docs_dict))

            cnt = cnt + 1

    file.write("]")
    file.close()

def split_test(files, dir="reserved_test"):
    """
    Resereves half of the validation data for usages other than spacy model creation.

    Parameters
    ----------
    files : list[str]
        list of file names in validation data
    dir : str
        name of directory to save reserved test data to

    Returns list of validation datat to use for spacy model creation
    """
    midpoint = len(files) // 2
    validate_reserve = files[midpoint:]
    validate_use = files[:midpoint]

    if not os.path.exists(dir):
        os.makedirs(dir)

    for file in validate_reserve:
        json_file = open(file)
        data = json.load(json_file)
        split_name = file.split("/")
        name = dir + "/" + split_name[len(split_name)-1]
        with open(name, 'w') as f:
            json.dump(data, f)
        json_file.close()

    return validate_use


def rawJsonToSpacyJson(dir=None, model="en_core_web_lg", suffix=".json", split=True, input_test_size=0.2,outputFileName=None,reserve_test=False,reserve_test_dir="Data/reserved_test"):
    """Add docstring"""

    # Walk through the directory and retrieve all files ending in fileSuffix
    path = os.walk(dir)
    filePaths = []
    for root, directories, files in path:
        for name in files:
            if name.endswith(suffix):
                filePaths.append(os.path.join(root, name))
        for name in directories:
            if name.endswith(suffix):
                filePaths.append(os.path.join(root, name))

    # Check to see if a user wants to split data into train, validate and test set
    if split:

        train, validate = train_test_split(filePaths, test_size=input_test_size, shuffle=True)

        if reserve_test:
            validate = split_test(validate, reserve_test_dir)

        trainFile = outputFileName+"_training_data.jsonl"
        validateFile = outputFileName + "_validate_data.jsonl"

        # Create training set
        convertJsonToSpacyJsonl(model,trainFile, train)

        # Create validate set
        convertJsonToSpacyJsonl(model,validateFile, validate)

    else:
        convertJsonToSpacyJsonl(model,outputFileName+".jsonl", filePaths)

if __name__ == "__main__":

    #
    # Parse out the arguments and assign them to variables
    #
    parser = argparse.ArgumentParser(
        description="convert raw JSON to the JSON format used by SpaCy for training ",
        epilog="Example: python3 json2SpacyJson.py jsonFolder outputFileName en_core_web_lg (optional --suffix '.json' ; --split True ; --test_size 0.2"
    )
    parser.add_argument(
        'jsonFolder', help='Folder containing json files'
    )
    parser.add_argument(
        'outputFileName', help='Output Filename'
    )
    parser.add_argument(
        'spacyModel', help='Spacy Model'
    )
    parser.add_argument(
        '--suffix', default=".json", type=str, help='Suffix the files ends in. Default=".json" '
    )
    parser.add_argument(
        '--split', help='Whether to split dataset into training, validation and test sets. Default = True'
    )
    parser.add_argument(
        '--test_size', help='Size of validate set. Should be a value between 0 and 1. Default = 0.2'
    )
    parser.add_argument(
        '--reserve_test', help='Whether to reserve half of test data. Default=False',
    )
    parser.add_argument(
        '--reserve_test_dir', help='Where to save reserved test data. Default=Data/reserved_test',
    )



    if len(sys.argv) < 3:
        parser.print_usage()
        sys.exit()

    args = parser.parse_args()

    if args.split.lower() == 'false':
        args.split = False
    else:
        args.split = True

    if args.test_size is None:
        args.test_size = 0.2
    else:
        args.test_size = float(args.test_size)

    if args.suffix is None:
        args.suffix = ".json"

    if args.reserve_test is None:
        args.reserved_test = False
    if args.reserve_test_dir is None:
        args.reserve_test_dir = "Data/reserved_test"

    rawJsonToSpacyJson(dir=args.jsonFolder, model=args.spacyModel, suffix=args.suffix, split=args.split, input_test_size=args.test_size,outputFileName=args.outputFileName, reserve_test=args.reserve_test, reserve_test_dir=args.reserve_test_dir)
