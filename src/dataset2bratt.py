from json2bratt import conversion
import glob
import argparse


def dataset_to_bratt(input_dir, output_dir, file_pattern="/*td.json", name_prefix=None):
    '''
    Converts a whole dataset into bratt and txt files.
    Must run from main directory, prefix feature not working yet.

    Parameters
    ----------
    file_dir : str
        directory of files to convert
    output_dir : str
        dirctory to output to
    file_pattern : str
        (optional) pattern of file endings in directory to select and convert
    name_prefix : str
        (optional) start of name for new bratt and json files
    '''
    files = glob.glob(input_dir+file_pattern)
    print("%s files to convert." % str(len(files)))

    for f in files:
        print("Converting %s..." % f)
        if name_prefix is None:
            prefix = f.split(".")[0].split("/")[2]
        else:
            prefix = name_prefix
        conversion(f, output_dir+"/"+prefix)

    print("Finished dataset conversion, new files in %s." % output_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Converts a dataset to bratt",
        epilog='python dataset2bratt.py input_dir output_dir'
    )
    parser.add_argument(
        'input_dir', help='path to files to convert'
    )
    parser.add_argument(
        'output_dir', help='path to output converted files'
    )

    parser.add_argument(
        '--file_pattern', help='file ending of files to convert',
        action='store', default="/*_td.json"
    )
    parser.add_argument(
            '--name_prefix', help='file name prefix for saving',
            action='store', default=None
    )

    args = parser.parse_args()
    input, output = args.input_dir, args.output_dir
    pattern, prefix = args.file_pattern, args.name_prefix

    dataset_to_bratt(input, output, file_pattern=pattern, name_prefix=prefix)
