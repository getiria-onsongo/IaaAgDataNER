#!/bin/env python3

from json2py import *
import glob

def combineJsonFiles(fprefix, fsuffix, input_dir, output_file, output_dir):
    """ Add docstring """
    " Name of the output file is the prefix out the input file with .jsonl added at the end."

    training_data = []
    for fname in glob.glob(input_dir+"/"+fprefix+'*'+fsuffix):
        data = json_2_dict(fname)
        train_data = dict_2_mixed_type(data)
        training_data.extend(train_data)

    fho = open(output_dir + "/" + output_file, 'w')

    train_data = dict_2_mixed_type(data)
    fho.write('TRAIN_DATA = ' + str(training_data) + "\n")

if __name__ == "__main__":

    #
    # Parse out the arguments and assign them to variables
    #
    parser = argparse.ArgumentParser(
        description="Convert json to training data list",
        epilog='Example: python3 json2TrainData.py barley_p _td_parag.json Data/DavisLJ11/parag barley_train_data.py Data/DavisLJ11/train_data'
    )
    parser.add_argument(
        'fprefix', help='File prefix for training data in json format.'
    )
    parser.add_argument(
        'fsuffix', help='File suffix for training data in json format.'
    )
    parser.add_argument(
        'input_dir', help='Input directory where the training data can be found.'
    )
    parser.add_argument(
        'output_file', help='Name of output file.'
    )
    parser.add_argument(
        'output_dir',
        help='Output directory (must exist already) to place output file in jsonl format.'
    )

    if len(sys.argv) < 5:
        parser.print_usage()
        sys.exit()

    args = parser.parse_args()
    fprefix, fsuffix, input_dir, output_file, output_dir = args.fprefix, args.fsuffix, args.input_dir, args.output_file, args.output_dir

    combineJsonFiles(fprefix, fsuffix, input_dir, output_file, output_dir)

