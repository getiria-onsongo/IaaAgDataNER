
def split_test(files, dir="reserved_val"):
    """
    Creates validation data besides spacy test. Possible use in json2spacyjson

    Parameters
    ----------
    files : list[str]
        list of file names in validation data
    dir : str
        name of directory to save reserved test data to

    Returns list of validation datat to use for spacy model creation
    """
    midpoint = len(files) // 2
    validate_reserve = files[midpoint:]
    validate_use = files[:midpoint]

    if not os.path.exists(dir):
        os.makedirs(dir)

    for file in validate_reserve:
        json_file = open(file)
        data = json.load(json_file)
        split_name = file.split("/")
        name = dir + "/" + split_name[len(split_name)-1]
        with open(name, 'w') as f:
            json.dump(data, f)
        json_file.close()

    return validate_use
