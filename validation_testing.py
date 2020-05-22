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

def leave_one_out_xval(maxn, fprefix, fsuffix, input_dir, output_dir, output_prefix):
   """ perform leave-one-out cross validation on the dataset. """

   for i in range(1, maxn+1):
       train_file = build_nth_dataset(i, maxn, fprefix, fsuffix, input_dir, output_dir, output_prefix)
       test_file = input_dir+"/"+fprefix+str(i)+fsuffix

       model_dir = train_nth_model(i, output_dir+"/"+output_prefix+str(i)+".json", output_dir, output_prefix)

       accuracyFile_name = model_dir+"_stats.txt"
       check_model_accuracy(test_file, model_dir, accuracyFile_name)
       clear_tally()
   
def train_nth_model(n, training_file, output_dir, outfile_prefix):
    """train nth spaCy model"""

    model_dir = output_dir+"/"+outfile_prefix+str(n)
    n_iter = 100
    trainModel(None, training_file, model_dir, n_iter)
    return model_dir

def build_nth_dataset(n, maxn, fprefix, fsuffix, input_dir, output_dir, outfile_prefix):
    """Build a JSON training set that excludes the nth among maxn entries."""

    local_data = dict()
    
    sys.stderr.write("Working on training segment "+str(n)+"\n")
    trainFile_name = output_dir+"/"+outfile_prefix+str(n)+".json"
    fo = open(trainFile_name, 'w')
    fo.write("[")
    
    for i in range(1, maxn+1):
        
        if (i != n):
            infile = input_dir+"/"+fprefix+str(i)+fsuffix

            with open(infile) as fi:
                local_data = json.load(fi)
            json.dump(local_data, fo)

            if ((n == maxn) and (i != maxn-1) or
                (n == maxn-1) and (i != maxn) or
                (n < maxn-1) and (i != maxn)):
                fo.write(", ")

    fo.write("]\n")

    return trainFile_name

if __name__ == "__main__":

    #
    # Parse out the arguments and assign them to variables
    #
    parser = argparse.ArgumentParser(
        description = "Perform leave one out validation for NER training",
        epilog = 'Example: python3 validation_testing.py maxn fprefix fsuffix input_dir output_dir output_prefix (optional --titrate)'
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
        '--titrate', help = 'Flag to perform experiments where the number of chuncks used in training is titrated from 1 all the way up to maxn-1. Default=False', action = 'store_true', default = False
    )

    if len(sys.argv)<5:
        parser.print_usage()
        sys.exit()
        
    args = parser.parse_args()
    maxn, fprefix, fsuffix, input_dir, output_dir, output_prefix, titrate = int(args.maxn), args.fprefix, args.fsuffix, args.input_dir, args.output_dir, args.output_prefix, args.titrate

    if titrate:
        for i in range(2, maxn+1):
            leave_one_out_xval(i, fprefix, fsuffix, input_dir, output_dir, output_prefix+'.'+str(i)+'.')
    else:
        leave_one_out_xval(maxn, fprefix, fsuffix, input_dir, output_dir, output_prefix)
    summarize_stats(output_dir+'/'+output_prefix)
