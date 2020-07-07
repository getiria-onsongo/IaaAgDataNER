#!/bin/env python3

import spacy
import re
import sys
import os
import json
import glob
import csv
import argparse
from nerTraining import *
from checkAccuracy import *
import subprocess
from sklearn.model_selection import train_test_split
from spacy.gold import biluo_tags_from_offsets
from spacy.gold import docs_to_json

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
        tags = biluo_tags_from_offsets(doc, entities)
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

def convert_to_biluo_tags(trainFile_name, input_test_size, train_file_name,validate_file_name):
    """ Add docstring """
    training_data = json_2_dict(trainFile_name)
    TRAIN_DATA = dict_2_mixed_type(training_data)
    train, validate = train_test_split(TRAIN_DATA,test_size=input_test_size)
    nlp = spacy.load('en_core_web_md')
    nerDataToJSON(train, train_file_name, nlp)
    nerDataToJSON(validate, validate_file_name, nlp)

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



def build_datasets(test_pages, maxn, fprefix, fsuffix, input_dir, output_dir, outfile_prefix):
    """Take as input two lists indicating pages to use for training and test set and
    create training and test sets."""

    sys.stderr.write("\n\n============================ Creating datasets ============================================\n")
    trainFile_name = output_dir + "/" + outfile_prefix + "_training_data.json"
    testFile_name = output_dir + "/" + outfile_prefix + "_test_data.json"
    num_test_pages = len(test_pages)
    num_train_pages = maxn - num_test_pages

    fo = open(trainFile_name, 'w')
    fo.write("[")
    num_train = 1
    for i in range(1, maxn + 1):
        if i not in test_pages:
            infile = input_dir + "/" + fprefix + str(i) + fsuffix
            with open(infile) as fi:
                local_data = json.load(fi)
            json.dump(local_data, fo)
            if (num_train < num_train_pages):
                fo.write(", ")
            num_train = num_train + 1
    fo.write("]\n")
    fo.close()

    fo = open(testFile_name, 'w')
    fo.write("[")
    num_test = 1
    for page_num in test_pages:
            infile = input_dir + "/" + fprefix + str(page_num) + fsuffix
            with open(infile) as fi:
                local_data = json.load(fi)
            json.dump(local_data, fo)
            if (num_test < num_test_pages):
                fo.write(", ")
            num_test = num_test + 1
    fo.write("]\n")
    fo.close()

    return trainFile_name, testFile_name

def train_model_pretrain(training_file,output_dir,outfile_prefix,test_size,pretrained_model,model_folder, n_iter = 1000, early_stop = 20):
    """train spaCy model"""
    sys.stderr.write("\n\n============================ Training Model ============================================\n")
    training_data_file_name = output_dir+"/"+outfile_prefix+"_cli_training_data.json"
    validate_data_file_name = output_dir+"/"+outfile_prefix+"_cli_validate_data.json"
    convert_to_biluo_tags(training_file,test_size,training_data_file_name,validate_data_file_name)
    train_cmd = "python3 -m spacy train en " + model_folder + " " + training_data_file_name + " " + validate_data_file_name + " --init-tok2vec " + pretrained_model + "  --vectors \"en_core_web_md\" --pipeline ner --n-iter " + str(n_iter) + " --n-early-stopping " + str(early_stop) + "  --debug"
    sys.stderr.write(train_cmd)
    execute(train_cmd)
    model = model_folder + "/model-best"
    return model



def test_model(test_pages_list, maxn, fprefix, fsuffix, input_dir, output_dir, output_prefix,pretrained_model,test_size):
   """ """
   train_file, test_file = build_datasets(test_pages_list, maxn, fprefix, fsuffix, input_dir, output_dir, output_prefix)
   model_folder = output_dir+"/"+output_prefix+"_model"

   model_dir = train_model_pretrain(train_file, output_dir, output_prefix, test_size, pretrained_model,model_folder)
   accuracyFile_name = model_folder+"_stats.txt"
   sys.stderr.write("\n\n============================ Checking model accuracy ============================================\n")
   check_model_accuracy(test_file, model_dir, accuracyFile_name)


if __name__ == "__main__":
    #
    # Parse out the arguments and assign them to variables
    #
    parser = argparse.ArgumentParser(
        description = "Perform leave one out validation for NER training",
        epilog = 'Example: python3 ner_model_testing.py maxn test_pages fprefix fsuffix input_dir output_dir output_prefix pretrained_model'
    )
    parser.add_argument(
        'maxn', help = 'integer for max chunks the training data is broken into'
    )

    parser.add_argument(
        'test_pages', help='Comma separated list of test pages'
    )

    parser.add_argument(
        'fprefix', help = 'File prefix for training data.'
    )
    parser.add_argument(
        'fsuffix', help = 'File suffix for training data.'
    )
    parser.add_argument(
        'input_dir', help = 'input directory where the training data can be found.'
    )
    parser.add_argument(
        'output_dir', help = 'Output directory (must exist already) to place for combined training file that includes all chunks except the ith one.'
    )
    parser.add_argument(
        'output_prefix', help = 'Output filename base prefix for combined training file that includes all chunks except the ith one.'
    )
    parser.add_argument(
        'pretrained_model',
        help='Folder with pre-trained model.'
    )

    if len(sys.argv)<6:
        parser.print_usage()
        sys.exit()
        
    args = parser.parse_args()
    maxn,test_pages,fprefix,fsuffix,input_dir,output_dir,output_prefix,pretrained_model = int(args.maxn),args.test_pages,args.fprefix, args.fsuffix, args.input_dir, args.output_dir, args.output_prefix, args.pretrained_model

    test_pages_list = []
    for page in test_pages.split(","):
        test_pages_list.append(int(page))
    test_model(test_pages_list, maxn, fprefix, fsuffix, input_dir, output_dir, output_prefix, pretrained_model,test_size=0.5)

    summarize_stats(output_dir+'/'+output_prefix)
