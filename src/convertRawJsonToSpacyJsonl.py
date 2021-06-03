#!/bin/env python3
import spacy

import warnings
from json2py import *
from sklearn.model_selection import train_test_split
from spacy.training import offsets_to_biluo_tags
from spacy.training import docs_to_json

def convertJsonToSpacyJsonl(outputFileName=None, filePaths=None):
    # Load spacy pipeline
    nlp = spacy.load('en_core_web_md')
    # Create a file to contain the jsonl format for SpaCy
    file = open(outputFileName, "w")
    file.write("[")
    cnt = 0

    # Iterate through each file
    for fileName in filePaths:
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

def rawJsonToSpacyJson(dir=None, fileSuffix=".json", splitTrainValidationTest=True, trainValidationTestRatio="0.7:0.2:0.1",outputFileName=None):
    """Add docstring"""

    # Walk through the directory and retrieve all files ending in fileSuffix
    path = os.walk(dir)
    filePaths = []
    for root, directories, files in path:
        for name in files:
            if name.endswith(fileSuffix):
                filePaths.append(os.path.join(root, name))
        for name in directories:
            if name.endswith(fileSuffix):
                filePaths.append(os.path.join(root, name))

    # Check to see if a user wants to split data into train, validate and test set
    if splitTrainValidationTest:
        dataSizes = trainValidationTestRatio.split(":")
        ratioTotal=float(dataSizes[0]) + float(dataSizes[1]) + float(dataSizes[2])

        if(ratioTotal < 0.999):
            dataSizes = trainValidationTestRatio.split("0.7:0.2:0.1")
            warnings.warn(''' Warning!: Fraction for the training, validation and test sets should add to 1 \n e.g., 
            "0.7:0.2:0.1". Default values of 0.7:0.2:0.1" used.''')

        validationRatio = float(dataSizes[1])
        testRatio = float(dataSizes[2])
        train, validateTest = train_test_split(filePaths, test_size=validationRatio+testRatio, shuffle=True)

        trainFile = outputFileName+"_training_data.jsonl"
        validateFile = outputFileName + "_validate_data.jsonl"
        inputs = [[trainFile,train]]

        # Check to see if a user wants a test set
        if(testRatio > 0):
            newSplit = testRatio/(validationRatio+testRatio)
            testFile = outputFileName + "_test_data.jsonl"
            validate, test = train_test_split(validateTest, test_size=newSplit, shuffle=True)
            inputs.append([validateFile, validate])
            inputs.append([testFile, test])
        else:
            inputs.append([validateFile,validateTest])

        # Loop through and create jsonl files for train, validate and test sets
        for vals in inputs:
            convertJsonToSpacyJsonl(vals[0], vals[1])
    else:
        convertJsonToSpacyJsonl(outputFileName+".jsonl", filePaths)

