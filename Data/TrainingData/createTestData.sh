#!/bin/bash

# This scripts takes training data from multiple sub-directories and creates
# a combined training dataset. Each PDF should be annotated its own directory
# At the moment, this scripts needs to be manually updated when a new folder
# is added. This is a short-term solution while we are proto-typing. If this
# project works, we will need to find a better solution.


# Create symbolic links for PDFs.
ln -s ../CSU/Bill-Brown-Reprint.pdf Bill-Brown-Reprint.pdf
ln -s ../CSU/Cowboy-reprint.pdf Cowboy-reprint.pdf
ln -s ../CSU/Ripper-Reprint.pdf Ripper-Reprint.pdf
ln -s ../UIdaho2019/small-grains-report_2019.pdf small-grains-report_2019.pdf
ln -s ../DavisLJ11/BarCvDescLJ11.pdf BarCvDescLJ11.pdf
# Add a line above for each new PDF

DirectoryArray=(
"../DavisLJ11"
"../CSU"
"../UIdaho2019"
)


# Add a path above for each new directory

# Counter to assign new page numbers
i=1

# Loop through folders and extract files ending in _td.json
for folder in ${DirectoryArray[*]}; do
    # Assign output from ls command to variable "files"
    files=$(ls -1 "$folder"/*"_td.json")
    # Create a symbolic link for each file
    for json in ${files[*]}; do
        # Create a symbolic link for .json file
        ln -s $json "dataset_p"$i"_td.json"

        # Replace .json with .py. We need to also create a symbolic link for .py file
        py=$(echo "$json" | sed -e 's/\.json/\.py/g')
        # Create a symbolic link for .py file
        ln -s $py "dataset_p"$i"_td.py"

        # Increment counter for new page numbers
        ((i=i+1))
    done
done

