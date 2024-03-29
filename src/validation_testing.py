#!/bin/env python3

import spacy
import re
import sys
import os
import json
import glob
import csv
import argparse
import random
import subprocess

from sklearn.model_selection import train_test_split
from spacy.training import offsets_to_biluo_tags
from spacy.training import docs_to_json

from checkAccuracy import *


def summarize_stats(fprefix):
    """ summarize accuracy statistics across all files in the series"""

    tally = dict()
    for fname in glob.glob(fprefix+'*'+'_stats.txt'):
        with open(fname) as fh:
            rd = csv.reader(fh, delimiter="\t")
            for row in rd:
                if row[0] != 'Entity':
                    try:
                        tally[row[0]]['total'] += int(row[2])
                    except KeyError:
                        tally[row[0]] = dict()
                        tally[row[0]]['total'] = int(row[2])
                    try:
                        tally[row[0]][row[1]] += int(row[2])
                    except KeyError:
                        tally[row[0]][row[1]] = int(row[2])

    # print combined stats
    sys.stderr.write("Entity\tStatus\tCount\tPercent\n")
    for label in tally:
        for state in tally[label]:
            if state != 'total':
                count = tally[label][state]
                total = tally[label]['total']
                pcnt = round(100*count/total, 1)
                sys.stderr.write(label+"\t"+state+"\t"+str(count)+"\t"+str(pcnt)+"\n")

def execute(cmd):
    """
        Takes as input a command to execute (cmd: str), executes the command and
        returns the exit code (exit_code)
    """
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout_data, stderr_data) = process.communicate()
    return_code = process.wait()

    if (return_code != 0):
        print("Error:", stderr_data)
        raise ValueError("Failed to execute command:", cmd)

    sys.stderr.write(stderr_data.decode())
    sys.stdout.write(stdout_data.decode())

def deleteFile(file_to_delete):
    """ Delete file"""
    delete_cmd = "rm -rf " + file_to_delete
    sys.stderr.write("\n"+delete_cmd+"\n")
    execute(delete_cmd)

def execute(cmd):
    """
        Takes as input a command to execute (cmd: str), executes the command and
        returns the exit code (exit_code)
    """
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout_data, stderr_data) = process.communicate()
    return_code = process.wait()

    if (return_code != 0):
        print("Error:", stderr_data)
        raise ValueError("Failed to execute command:", cmd)

    sys.stderr.write(stderr_data.decode())
    sys.stdout.write(stdout_data.decode())

def nerDataToJSON(data, fileName,nlp):
    ''' Take as input ner training data and convert it into
    CLI json training data.'''
    # nlp = spacy.load('en_core_web_md')
    file = open(fileName, "w")
    file.write("[")
    cnt = 0
    for entry in data:
        rawText = entry[0]
        #rawText = rawText.strip()
        #rawText = rawText.replace('"','')
        #rawText = rawText.replace("'", "")
        doc = nlp(rawText)
        entities = entry[1]['entities']
        #tags = biluo_tags_from_offsets(doc, entities)
        # Changes in SpaCy 3
        tags = offsets_to_biluo_tags(doc, entities)
        docs_dict = docs_to_json([doc], cnt)
        for i in range(len(docs_dict['paragraphs'][0]['sentences'][0]['tokens'])):
            docs_dict['paragraphs'][0]['sentences'][0]['tokens'][i]['ner'] = tags[i]
        if(cnt > 0):
            file.write(",")
            file.write("\n")
        file.write(json.dumps(docs_dict))

        cnt = cnt + 1
    file.write("]")
    file.close()

def convert_to_biluo_tags(dataset_file,input_test_size,output_dir,data_prefix):
    """ Add docstring """

    training_data = json_2_dict(dataset_file)
    TRAIN_DATA = dict_2_mixed_type(training_data)
    train, validate = train_test_split(TRAIN_DATA,test_size=input_test_size)

    train_file_json = output_dir + "/" + data_prefix + "_train.json"
    dev_file_json = output_dir + "/" + data_prefix + "_dev.json"
    nlp = spacy.load('en_core_web_sm')
    nerDataToJSON(train, train_file_json, nlp)
    nerDataToJSON(validate, dev_file_json, nlp)

    convert_train_cmd = "python -m spacy convert --converter json "+train_file_json+" "+output_dir
    sys.stderr.write("\n"+convert_train_cmd+"\n")
    execute(convert_train_cmd)

    convert_dev_cmd = "python -m spacy convert --converter json " + dev_file_json + " " + output_dir
    sys.stderr.write("\n"+convert_dev_cmd+"\n")
    execute(convert_dev_cmd)

    # After conversion, spacy will create binary files ending in .spacy in output_dir
    train_file_spacy = output_dir + "/" + data_prefix + "_train.spacy"
    dev_file_spacy = output_dir + "/" + data_prefix + "_dev.spacy"
    return[train_file_spacy,dev_file_spacy]


def train_nth_model(n, dataset_file, output_dir, outfile_prefix, test_size):
    """Build a JSON training set that excludes the nth among maxn entries.
    NOTE: The recommended training approach as off SpaCy 3 is to use the CLI. The training
    pipeline requires development data in addition to training data. Development data is another
    name for evaluation data. It is used to evaluate how the model being trained is performing
    on unseen examples. The accuracy metrics SpaCy gives when training is based on performance on
    the development (evaluation) data."""

    data_prefix = outfile_prefix+str(n)
    [train_file,dev_file] = convert_to_biluo_tags(dataset_file,test_size,output_dir,data_prefix)

    # Create a config file to use for training
    config_file_name = output_dir + "/" + data_prefix + ".cfg"
    create_config_cmd = "python -m spacy init config "+config_file_name+" --lang \"en\" --pipeline \"ner\" --optimize \"accuracy\" --force "
    sys.stderr.write("\n"+create_config_cmd+"\n")
    execute(create_config_cmd)

    # Train model
    train_cmd = "python -m spacy train "+config_file_name+" --output "+output_dir+" --paths.train "+train_file+" --paths.dev "+dev_file
    sys.stderr.write("\n"+train_cmd+"\n")
    execute(train_cmd)
    model = output_dir + "/model-best"
    return model


def build_nth_dataset(n, maxn, fprefix, fsuffix, input_dir, output_dir, outfile_prefix):
    """Build a JSON training set that excludes the nth among maxn entries."""

    sys.stderr.write("\n\n============================ Testing segment " + str(n) + " ===========================\n")
    trainFile_name = output_dir + "/" + outfile_prefix + str(n) + ".json"
    fo = open(trainFile_name, 'w')
    fo.write("[")
    for i in range(1, maxn + 1):
        if (i != n):
            infile = input_dir + "/" + fprefix + str(i) + fsuffix

            with open(infile) as fi:
                local_data = json.load(fi)
            json.dump(local_data, fo)

            if ((n == maxn) and (i != maxn - 1) or
                    (n == maxn - 1) and (i != maxn) or
                    (n < maxn - 1) and (i != maxn)):
                fo.write(", ")

    fo.write("]\n")
    fo.close()
    return trainFile_name

def leave_one_out_xval(maxn, fprefix, fsuffix, input_dir, output_dir, output_prefix,validate,test_size):
   """ perform leave-one-out cross validation on the dataset. """
   if (not validate):
       test_page = random.randint(1, maxn)
       test_file = input_dir + "/" + fprefix + str(test_page) + fsuffix
       dataset_file = build_nth_dataset(test_page, maxn, fprefix, fsuffix, input_dir, output_dir, output_prefix)
       model_dir = train_nth_model(test_page, dataset_file, output_dir, output_prefix, test_size)
       accuracyFile_name = output_dir + "/" + output_prefix + str(test_page)+"_stats.txt"
       check_model_accuracy(test_file, model_dir, accuracyFile_name)
   else:
       print("Run the validate code")
       for i in range(1, maxn + 1):
           test_file = input_dir + "/" + fprefix + str(i) + fsuffix
           dataset_file = build_nth_dataset(i, maxn, fprefix, fsuffix, input_dir, output_dir, output_prefix)
           model_dir = train_nth_model(i, dataset_file, output_dir, output_prefix, test_size)
           accuracyFile_name = output_dir + "/" + output_prefix + str(i) + "_stats.txt"
           check_model_accuracy(test_file, model_dir, accuracyFile_name)
           clear_tally()
           # Delete temp files to save space
           deleteFile(output_dir + "/" + output_prefix + str(i) + ".cfg")
           deleteFile(output_dir + "/" + output_prefix + str(i) + ".json")
           deleteFile(output_dir + "/" + output_prefix + str(i) + "_dev.json")
           deleteFile(output_dir + "/" + output_prefix + str(i) + "_dev.spacy")
           deleteFile(output_dir + "/" + output_prefix + str(i) + "_train.json")
           deleteFile(output_dir + "/" + output_prefix + str(i) + "_train.spacy")
           deleteFile(output_dir + "/model-best")
           deleteFile(output_dir + "/model-last")


if __name__ == "__main__":

    #
    # Parse out the arguments and assign them to variables
    #
    # NOTE: The --validate flag is used if you want to perform leave-one-out cross validation. Because
    # training is time consuming, for testing purposes do not use the --validate flag. Not using the --validate flag
    # will result in a single analysis being performed where one of the pages in randomly chosen and used at the
    # test page and the other pages are use for training. This is sufficient to test the code.
    #
    # Also note, the training will converge faster if you use more data. If the folder with your data contains 37 training pages
    # we recommend setting maxn to 37.
    # e.g., > python src/validation_testing.py 37 'barley_p' '_td.json' Data/DavisLJ11  /tmp/spacy 'test_'
    #
    parser = argparse.ArgumentParser(
        description="Perform leave one out validation for NER training",
        epilog='Example: python validation_testing.py maxn fprefix fsuffix input_dir output_dir output_prefix (optional --validate)'
    )
    parser.add_argument(
        'maxn', help='integer for max chunks the training data is broken into'
    )
    parser.add_argument(
        'fprefix', help='File prefix for training data.'
    )
    parser.add_argument(
        'fsuffix', help='File suffix for training data.'
    )
    parser.add_argument(
        'input_dir', help='input directory where the training data can be found.'
    )
    parser.add_argument(
        'output_dir',
        help='Output directory (must exist already) to place for combined training file that includes all chunks except the ith one.'
    )
    parser.add_argument(
        'output_prefix',
        help='Output filename base prefix for combined training file that includes all chunks except the ith one.'
    )
    parser.add_argument(
        '--validate',
        help='Flag to perform leave one out cross-validation. Default=False which does a single test using one of the pages as the test page.',
        action='store_true', default=False
    )

    if len(sys.argv) < 5:
        parser.print_usage()
        sys.exit()

    args = parser.parse_args()
    maxn, fprefix, fsuffix, input_dir, output_dir, output_prefix, validate = int(args.maxn), args.fprefix, args.fsuffix, args.input_dir, args.output_dir, args.output_prefix,  args.validate

    leave_one_out_xval(maxn, fprefix, fsuffix, input_dir, output_dir, output_prefix, validate, test_size=0.2)

    print("Summarizing statistics")
    summarize_stats(output_dir + '/' + output_prefix)
