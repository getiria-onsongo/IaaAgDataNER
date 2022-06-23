from jsontobratt import conversion
import glob


def dataset_to_bratt(file_dir, file_pattern="/*_td.json", output_dir="Data/Input/"):
    files = glob.glob(file_dir+file_pattern)
    print("%s files to convert." %str(len(files)))
    print("_________________________")

    for f in files:
        print("Converting %s..." %f)
        name_prefix = f.split(".")[0].split("/")[2]
        conversion(f, output_dir+name_prefix)

    print("Finished dataset conversion, new files in %s." %output_dir)
    print("_________________________")
