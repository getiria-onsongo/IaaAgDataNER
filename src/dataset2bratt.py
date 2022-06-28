from json2bratt import conversion
import glob
import argparse
import os

def extract_page_num(f, suffix):
    num = 'error'
    if f[len(f)-(len(suffix)+1)] in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
        num = f[len(f)-(len(suffix)+1)]
        if f[len(f)-(len(suffix)+2)] in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
            num = f[len(f)-(len(suffix)+2)] + num
    return num


def dataset_to_bratt(input_dir, output_dir, file_pattern="/*_td.json", name_prefix=None):
    '''
    Converts a whole dataset into bratt and txt files.

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
    print(files)
    print("%s files to convert." % str(len(files)))

    for f in files:
        print("Converting %s..." % f)
        path_no_suffix = f.split(".")[0].split("/")
        prefix = path_no_suffix[len(path_no_suffix)-1]
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

    args = parser.parse_args()
    input, output = args.input_dir, args.output_dir
    pattern, prefix = args.file_pattern, args.name_prefix

    if not os.path.exists(input):
        print("input dataset path does not exist")
    else:
        if not os.path.exists(output):
            os.makedirs(output)

        dataset_to_bratt(input, output, file_pattern=pattern)
