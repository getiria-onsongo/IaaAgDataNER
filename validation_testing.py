#!/bin/env python3

import spacy
import re
import sys
import argparse

def build_nth_dataset(n, maxn, fprefix, fsuffix, input_dir, outfile_prefix):
    """Build a python training set that excludes the nth among maxn entries."""

    fo = open(outfile_prefix+str(n)+".py", 'w')
    fo.write("TRAIN_DATA = [\n")
    
    for i in range(1, maxn+1):
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
        'output_prefix', help = 'Output path including prefix for combined training file that includes all chunks except the ith one.'
    )

    if len(sys.argv)<5:
        parser.print_usage()
        sys.exit()
        
    args = parser.parse_args()
    maxn, fprefix, fsuffix, input_dir, output_prefix = int(args.maxn), args.fprefix, args.fsuffix, args.input_dir, args.output_prefix

    for i in range(1, maxn+1):
        build_nth_dataset(i, maxn, fprefix, fsuffix, input_dir, output_prefix)



