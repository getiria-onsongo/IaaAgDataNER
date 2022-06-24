from json2bratt import conversion
import glob


def dataset_to_bratt(file_dir, output_dir, file_pattern="/*_td.json", name_prefix=None):
    '''
    Converts a whole dataset into bratt and txt files

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
    files = glob.glob(file_dir+file_pattern)
    print("%s files to convert." % str(len(files)))

    for f in files:
        print("Converting %s..." % f)
        if name_prefix == None:
            name_prefix = f.split(".")[0].split("/")[2]
        conversion(f, output_dir+"/"+name_prefix)

    print("Finished dataset conversion, new files in %s." % output_dir)
