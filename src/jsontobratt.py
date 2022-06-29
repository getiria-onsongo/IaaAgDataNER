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
    infile = tkinter.filedialog.askopenfilename(initialdir=["../Data"], filetypes=[("json files", "*.json *.jsonl")])
    root.destroy()
    outfile = input("\nName your output file: ")



def conversion(infile, outfile):
    annfile = outfile + ".ann"
    txtfile = outfile + ".txt"

    # If statement checks if the file exists and deletes it because the files will be appended not overwritten
    if os.path.exists(annfile):
        os.remove(annfile)
        print(f"\n{annfile} exists so it will be overwritten")
    if os.path.exists(txtfile):
        os.remove(txtfile)
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
        "ALAS": "varietal alias",
        "CROP": "crop",
        "CVAR": "crop_variety",
        "JRNL": "journal reference",
        "PATH": "pathogen",
        "PED": "pedigree",
        "PLAN": "plant anatomy",
        "PPTD": "plant predisposition to disease",
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
                    substring = x[int(entitydata[1].replace(",", "")): int(entitydata[3].replace(",", ""))]

                    # File is outputted in this formatted seen below
                    t_entry = f"t{tindx}\t{keyterm_long} {startnum} {endnum}\t{substring}"

                    # Finally it's written here into the ann file
                    with open(annfile, "a") as f:
                        f.write(t_entry)
                        f.write("\n")

                else:
                    print(f"\n{x} sentence has been skipped because, \033[91m\033[1m{keyterm}\033[0m \033[91mis not defined in the dictionary\033[0m")
                    with open(annfile, "a") as f:
                        f.write(f"Unknown key term {keyterm}")
                        f.write("\n")

            # Exception if the sentence has not been formatted properly
            except:
                raise ValueError(f"\033[91m{x}\033[0m is not formatted correctly so it has been skipped")

            tindx += 1
            counter += len(x)
            i += 1
        # Text file is written here and joined without any space
        with open(txtfile, "a") as f:
            f.write(x)
    print(f"\nFile converted to bratt as {annfile} and {txtfile}")


# Calls the method if the script is getting executed directly
if __name__ == "__main__":
    conversion(infile, outfile)
