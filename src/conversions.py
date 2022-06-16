import json
import os.path
import tkinter.filedialog

if __name__ == "__main__":
    root = tkinter.Tk()
    infile = tkinter.filedialog.askopenfilename(initialdir=["../Data"], filetypes=[("json files", "*.json *.jsonl")])
    root.destroy()
if __name__ == "__main__":
    annfile = input("\nName your ann file: ")
    outfile = annfile + ".ann"



def conversion(infile, outfile):
        if os.path.exists(outfile):
            os.remove(outfile)
        with open(infile) as f:
            data = json.load(f)

        data2 = data['sentences'].keys()
        counter = 0
        tindx = 1
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
        for x in data2:
            i = 1
            while i <= len(data['sentences'][x]):
                try:
                    entity = data['sentences'][x]['entity ' + str(i)]

                    irr = str(entity).split(" ")
                    startnum = int(irr[1].replace(",", "")) + counter
                    endnum = int(irr[3].replace(",", "")) + counter
                    keyterm = irr[5].replace("'", "").replace("}", "")
                    keyterm_long = keyterm_dict.get(keyterm, None)
                    substring = x[int(irr[1].replace(",", "")): int(irr[3].replace(",", ""))]
                    # print(str(startnum) + " " + str(endnum) + " " + " " + sentence)
                    t_entry = f"t{tindx}\t{keyterm_long} {startnum} {endnum}\t{substring}"
                    with open(outfile, "a") as f:
                        f.write(t_entry)
                        f.write("\n")
                except:
                    raise ValueError(x + "is not formatted correctly so it has been skipped")
                tindx += 1
                counter += len(x)
                i += 1
        print("\nFile converted to csv")

if __name__ == "__main__":
    conversion(infile, outfile)
