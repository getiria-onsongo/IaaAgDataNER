#!/bin/env python3

import spacy
import re
import sys
import os
import json
import argparse
from nerTraining import *
from checkAccuracy import *
import subprocess

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
        epilog = 'Example: python3 validation_testing.py maxn fprefix fsuffix input_dir output_dir output_prefix'
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

    if len(sys.argv)<5:
        parser.print_usage()
        sys.exit()
        
    args = parser.parse_args()
    maxn, fprefix, fsuffix, input_dir, output_dir, output_prefix = int(args.maxn), args.fprefix, args.fsuffix, args.input_dir, args.output_dir, args.output_prefix

    for i in range(1, maxn+1):
        train_file = build_nth_dataset(i, maxn, fprefix, fsuffix, input_dir, output_dir, output_prefix)

#        model_dir = train_nth_model(i, output_dir+"/"+output_prefix+str(i)+".json", output_dir, output_prefix)

#        accuracyFile_name = model_dir+"_stats.txt"
#        check_model_accuracy(train_file, model_dir, accuracyFile_name)
