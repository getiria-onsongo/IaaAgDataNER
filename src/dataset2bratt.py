from json2bratt import conversion
import glob
import argparse
import os

"""
File to convert a json dataset to bratt, also has page number extraction helper
function

Functions
-------
extract_page_num(self, f : str, suffix : str) -> str
    for file names with page numbers before the suffix, extracts the numerals
dataset_to_bratt(input_dir : str, output_dir : str, file_pattern : str)
    converts a json dataset to bratt format
"""

def extract_page_num(f : str, suffix : str) -> str:
    """
    Gets page number for files where the page numbers are the one or two
    positive integers found directly before the file suffix

    Parameters
    ----------
    f : str
        file name
    suffix : str
        file ending

    Returns page number as string, otherwise returns empty string
    """
    num = ""
    if f[len(f)-(len(suffix)+1)].isdigit():
        num = f[len(f)-(len(suffix)+1)]
        if f[len(f)-(len(suffix)+2)].isdigit():
            num = f[len(f)-(len(suffix)+2)] + num
    return num

def dataset_to_bratt(input_dir : str, output_dir : str, file_pattern="/*_td.json"):
    """
    Converts a whole dataset into bratt and txt files.

    Parameters
    ----------
    file_dir : str
        directory of files to convert
    output_dir : str
        dirctory to output to
    file_pattern : str
        pattern of file endings in directory to select and convert,
        default is "/*_td.json"
    name_prefix : str
        start of name for new bratt and json files
    """
    files = glob.glob(input_dir+file_pattern)
    print("%s files to convert." % str(len(files)))

    for f in files:
        print("Converting %s..." % f)
        path_no_suffix = f.split(".json")[0].split("/")
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
    input, output, pattern = args.input_dir, args.output_dir, args.file_pattern

    if not os.path.exists(input):
        print("input dataset path does not exist")
    else:
        if not os.path.exists(output):
            os.makedirs(output)
        dataset_to_bratt(input, output, file_pattern=pattern)
