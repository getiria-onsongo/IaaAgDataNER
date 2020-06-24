#!/bin/env python3

import json
import sys
import argparse
import glob

def json2raw(json_file_name, fhandler):
    """ Add docstring """

    f = open(json_file_name)
    data = json.load(f)
    f.close()

    cnt = 0
    for key in data['sentences'].keys():
        fhandler.write("{\"text\":\"" + key + "\"}")
        fhandler.write("\n")
        cnt = cnt + 1
    print("Converted " + str(cnt) + " sentences in file: " + json_file_name)
def convert_files(fprefix, fsuffix, input_dir, output_dir, output_prefix):
    """ Add docstring """
    " Name of the output file is the prefix out the input file with .jsonl added at the end."

    fhandler = open(output_dir + "/" + output_prefix+".jsonl", "w")
    for fname in glob.glob(input_dir+"/"+fprefix+'*'+fsuffix):
        json2raw(fname,fhandler)
    fhandler.close()

if __name__ == "__main__":
    #
    # Parse out the arguments and assign them to variables
    #
    parser = argparse.ArgumentParser(
        description="Create raw text for pre-training in jsonl format",
        epilog='Example: python3 json2rawText.py barley_p _td.json temp temp_out barley_raw_text'
    )
    parser.add_argument(
        'fprefix', help='File prefix for training data in json format.'
    )
    parser.add_argument(
        'fsuffix', help='File suffix for training data in json format.'
    )
    parser.add_argument(
        'input_dir', help='input directory where the training data can be found.'
    )
    parser.add_argument(
        'output_dir',
        help='Output directory (must exist already) to place output file in jsonl format.'
    )

    parser.add_argument(
        'output_prefix',
        help='Output filename base prefix for combined raw text from all json files.'
    )


    if len(sys.argv) < 5:
        parser.print_usage()
        sys.exit()

    args = parser.parse_args()
    fprefix, fsuffix, input_dir, output_dir, output_prefix =  args.fprefix, args.fsuffix, args.input_dir, args.output_dir, args.output_prefix

    convert_files(fprefix, fsuffix, input_dir, output_dir, output_prefix)