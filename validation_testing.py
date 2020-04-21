#!/bin/env python3

import spacy
import re
import sys
import os
import argparse
from nerTraining import *
import subprocess

def train_nth_model(n, output_dir, outfile_prefix):
    """train nth spaCy model"""

    model_dir = output_dir+"/"+outfile_prefix+str(n)
    n_iter = 100
    trainModel(None, model_dir, n_iter)
    return model_dir

def build_nth_dataset(n, maxn, fprefix, fsuffix, input_dir, output_dir, outfile_prefix):
    """Build a python training set that excludes the nth among maxn entries."""

    trainFile_name = output_dir+"/"+outfile_prefix+str(n)+".py"
    fo = open(trainFile_name, 'w')
    fo.write("TRAIN_DATA = [\n")
    
    for i in range(1, maxn+1):
        sys.stderr.write("Working on training segment "+str(i)+"\n")
        
        if (i != n):
            infile = input_dir+"/"+fprefix+str(i)+fsuffix

            fi = open(infile, 'r') 
            for line in fi:
                # output file doesn't need TRAIN_DATA and closing ']' internally
                if ((line.find('TRAIN_DATA') == -1) and
                    (line != ']\n')):

                    # replace last ')' with '),' in each intermediary file
                    # except the last (maxn+1th) one
                    if re.search(r'\)$', line) and (i != maxn):
                        line = re.sub(r'\)$', '),', line)
                    
                    fo.write(line)

    fo.write(']\n')
    fo.close()
    return trainFile_name

if __name__ == "__main__":

    #
    # Parse out the arguments and assign them to variables
    #
    parser = argparse.ArgumentParser(
        description = "Perform leave one out validation for NER training",
        epilog = 'Example: python3 validation_testing.py maxn fprefix fsuffix input_dir output_prefix'
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

        os.chdir(output_dir)
        print("output_dir: "+output_dir)
        training_data = __import__(output_prefix+str(i))
        TRAIN_DATA = training_data.TRAIN_DATA
        print("TRAIN_DATA:", TRAIN_DATA[0])

        model_dir = train_nth_model(i, output_dir, output_prefix)
        accuracyFile_name = model_dir+"_stats.txt"
        fh_acc = open(accuracyFile_name, 'w')
        subprocess.run(["python3", "checkAccuracy.py", model_dir, train_file], stdout=fh_acc)
