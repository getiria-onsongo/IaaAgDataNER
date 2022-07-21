'''Documentation
This is a json to bratt(ann) and text file converter
It loads the json file and uses key in the nested dictionary
Ann file uses Tindex \tabKeyterm start end \tabSentence
The text file just combines all the sentences into one paragraph
To use the program directly you would be asked for an input json file and asked to name both the ann and the txt file on one input
If you are calling the function you would add the location of the json file and just the prefix
'''

import json
import os.path
import tkinter.filedialog

# Checks if the python file is getting executed directly or getting called
if __name__ == "__main__":
    # Use tkinter for selecting files using a gui file selector
    root = tkinter.Tk()
    infile = tkinter.filedialog.askopenfilename(
        initialdir=["../Data"], filetypes=[("json files", "*.json *.jsonl")])
    root.destroy()
    outfile = input("\nName your output file: ")


def conversion(infile, outfile, sentence_level=False, print_statements=False):
    annfile = outfile + ".ann"
    txtfile = outfile + ".txt"

    # If statement checks if the file exists and deletes it because the files will be appended not overwritten
    if os.path.exists(annfile):
        os.remove(annfile)
        if print_statements:
            print(f"\n{annfile} exists so it will be overwritten")
    if os.path.exists(txtfile):
        os.remove(txtfile)
        if print_statements:
            print(f"{annfile} exists so it will be overwritten")
            print()
    # Load the json file
    with open(infile) as f:
        data = json.load(f)

    # First spilt the data by the sentences
    data2 = data['sentences'].keys()

    counter = 0
    tindx = 1

    # Key terms for all the labels in the json file
    keyterm_dict = {
        "ALAS": "varietal_alias",
        "CROP": "crop",
        "CVAR": "crop_variety",
        "JRNL": "journal_reference",
        "PATH": "pathogen",
        "PED": "pedigree",
        "PLAN": "plant_anatomy",
        "PPTD": "plant_predisposition_to_disease",
        "TRAT": "trait",
        # not complete for given CSV!
    }
    # For each loop to list out the sentences
    for x in data2:
        i = 1
        while i <= len(data['sentences'][x]):
            try:
                # Taking out the entities by using a while
                entity = data['sentences'][x]['entity ' + str(i)]

                # Split the entity datas and store into an array
                entitydata = str(entity).split(" ")

                # startnum and endnum add the length of the sentences the come before them

                startnum = int(entitydata[1].replace(",", "")) + counter
                endnum = int(entitydata[3].replace(",", "")) + counter
                keyterm = entitydata[5].replace("'", "").replace("}", "")

                # Replace the label using the keyterm dictionary above
                keyterm_long = keyterm_dict.get(keyterm, None)
                # If keyterm exists then print it out or print "unknown keyterm"
                if keyterm_long:
                    substring = x[int(entitydata[1].replace(",", "")): int(
                        entitydata[3].replace(",", ""))]

                    substring = substring.replace("\n", " ")
                    # File is outputted in this formatted seen below
                    t_entry = f"T{tindx}\t{keyterm} {startnum} {endnum}\t{substring}"

                    # Finally it's written here into the ann file
                    with open(annfile, "a") as f:
                        f.write(t_entry)
                        f.write("\n")

                else:
                    if print_statements:
                        print(f"\n{x} sentence has been skipped because, \033[91m\033[1m{keyterm}\033[0m is not defined in the dictionary")

            # Exception if the sentence has not been formatted properly
            except:
                raise ValueError(f"\033[91m{x}\033[0m is not formatted correctly so it has been skipped")

            tindx += 1
            i += 1

        # Text file is written here and joined without any space
        with open(txtfile, "a") as f:
            f.write(x)
        # This is the part which decides if you wanna do document or sentence level
        if sentence_level:
            counter += len(x)
        else:
            counter = 0

    print(f"File converted to bratt as {annfile} and {txtfile}")


# Calls the method if the script is getting executed directly
if __name__ == "__main__":
    conversion(infile, outfile)
