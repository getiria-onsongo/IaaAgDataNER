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


def build_nth_dataset(n, maxn, fprefix, fsuffix, input_dir, output_dir, outfile_prefix):
    """Build a JSON training set that excludes the nth among maxn entries."""

    sys.stderr.write("\n\n============================ Working on segment " + str(n) + " ===========================\n")
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

def train_nth_model(n, training_file, output_dir, outfile_prefix, test_size,pretrained_model, base_model, model_folder):
    """train nth spaCy model"""
    n_iter = 1000
    early_stop = 20
    training_data_file_name = output_dir+"/"+outfile_prefix+str(n)+"_training_data.json"
    validate_data_file_name = output_dir+"/"+outfile_prefix+str(n)+"_validate_data.json"

    convert_to_biluo_tags(training_file,test_size,training_data_file_name,validate_data_file_name)

    # ### NOTE: Validation is failing for some of the data because spacy considered entities with a space
    # as being in valid. Some of our entities have spaces in them
    #
    #validate_cmd = "python3 -m spacy debug-data en "+training_data_file_name+" "+validate_data_file_name+" -b \"en_core_web_md\" -p ner -V"
    #sys.stderr.write(validate_cmd)
    #execute(validate_cmd)
    train_cmd = "python3 -m spacy train en " + model_folder + " " + training_data_file_name + " " + validate_data_file_name + " --init-tok2vec " + pretrained_model + "  --vectors \"en_core_web_md\" --pipeline ner --n-iter " + str(n_iter) + " --n-early-stopping " + str(early_stop) + "  --debug"

    '''
    if (n > 1):
        train_cmd = "python3 -m spacy train en " + model_folder + " " + training_data_file_name + " " + validate_data_file_name + " --base-model " + base_model + " --init-tok2vec " + pretrained_model + "  --vectors \"en_core_web_md\" --pipeline ner --n-iter " + str(n_iter) + " --n-early-stopping " + str(early_stop) + "  --debug"

    else:
        train_cmd = "python3 -m spacy train en " +model_folder + " " + training_data_file_name + " " + validate_data_file_name + " --init-tok2vec "+pretrained_model+ "  --vectors \"en_core_web_md\" --pipeline ner --n-iter " + str(n_iter) + " --n-early-stopping " + str(early_stop) + "  --debug"
    '''
    sys.stderr.write(train_cmd)
    execute(train_cmd)
    model = model_folder + "/model-best"
    return model

def deleteFolder(folder_to_delete):
    """ Delete folder"""
    delete_cmd = "rm -rf " + folder_to_delete
    sys.stderr.write(delete_cmd)
    execute(delete_cmd)

def leave_one_out_xval(maxn, fprefix, fsuffix, input_dir, output_dir, output_prefix,pretrained_model,test_size):
   """ perform leave-one-out cross validation on the dataset. """
   for i in range(1, maxn+1):
       train_file = build_nth_dataset(i, maxn, fprefix, fsuffix, input_dir, output_dir, output_prefix)
       test_file = input_dir + "/" + fprefix + str(i) + fsuffix
       # Delete model folder no longer being used. Models consume a lot of disk space (about 1GB a model)
       if i > 2:
           deleteFolder(output_dir+"/"+output_prefix+"_model_"+str(i-2))
           deleteFolder(output_dir+"/"+output_prefix+str(i-2)+"_training_data.json")
           deleteFolder(output_dir+"/"+output_prefix+str(i-2)+"_validate_data.json")
           deleteFolder(output_dir + "/" + output_prefix + str(i - 2) + ".json")

       model_folder = output_dir+"/"+output_prefix+"_model_"+str(i)
       prev_model = output_dir+"/"+output_prefix+"_model_"+str(i-1) + "/model-best"
       model_dir = train_nth_model(i, train_file, output_dir, output_prefix, test_size, pretrained_model,prev_model, model_folder)

       accuracyFile_name = model_folder+"_stats.txt"
       check_model_accuracy(test_file, model_dir, accuracyFile_name)
       clear_tally()

if __name__ == "__main__":
    #
    # Parse out the arguments and assign them to variables
    #
    parser = argparse.ArgumentParser(
        description = "Perform leave one out validation for NER training",
        epilog = 'Example: python3 validation_testing.py maxn fprefix fsuffix input_dir output_dir output_prefix pretrained_model (optional --titrate)'
    )
    parser.add_argument(
        'maxn', help = 'integer for max chunks the training data is broken into'
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
    parser.add_argument(
        '--titrate', help = 'Flag to perform experiments where the number of chuncks used in training is titrated from 1 all the way up to maxn-1. Default=False', action = 'store_true', default = False
    )

    if len(sys.argv)<6:
        parser.print_usage()
        sys.exit()
        
    args = parser.parse_args()
    maxn, fprefix, fsuffix, input_dir, output_dir, output_prefix, pretrained_model, titrate = int(args.maxn), args.fprefix, args.fsuffix, args.input_dir, args.output_dir, args.output_prefix, args.pretrained_model,args.titrate

    if titrate:
        for i in range(2, maxn+1):
            leave_one_out_xval(i, fprefix, fsuffix, input_dir, output_dir, output_prefix+'.'+str(i)+'.',pretrained_model,test_size=0.1)
    else:
        leave_one_out_xval(maxn, fprefix, fsuffix, input_dir, output_dir, output_prefix,pretrained_model,test_size=0.1)

    print("Summarizing statistics")
    summarize_stats(output_dir+'/'+output_prefix)
