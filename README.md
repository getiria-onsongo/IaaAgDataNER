# IaaAgDataNER
Parse and categorize agricultural related data

## Background
So far, the approach has been to take the existing spaCy English trained
model and to build on it so that its Named Entity Recognizer (NER) can
recognize instances of the following agricultural terms:
- ALAS = varietal alias
- CROP = crop
- CVAR = crop_variety
- JRNL = journal reference
- PATH = pathogen
- PED  = pedigree
- PLAN = plant anatomy
- PPTD = plant predisposition to disease
- TRAT = trait

We are starting out by training the NER on the 37 pages of
[BarCvDescLJ11.pdf](https://smallgrains.ucdavis.edu/cereal_files/BarCvDescLJ11.pdf),
a compendium of barley varieties.

## Getting started
You can test the accuracy of the NER training with only N pages of the 37 page document. You will see that with only 5 pages, accuracy is good. Check for yourself!
```
git clone https://github.com/getiria-onsongo/IaaAgDataNER
cd IaaAgDataNER
mkdir /tmp/spacy
python3 validation_testing.py 5 'barley_p' '_td.json' Data/DavisLJ11 /tmp/spacy 'test_'
# To send output to a file (test_results.txt) instead of STDERR
python3 validation_testing.py 5 'barley_p' '_td.json' Data/DavisLJ11 /tmp/spacy 'test_' 2> test_results.txt
```
This will generate 5 JSON training files in `/tmp/spacy`: one that has
pages 2-5, one with page 1 and 3-5, one with pages 1-2 and 4-5, etc. A
model directory is created for each, and training accuracy stats are computed
for each one as well. Finally a compilation of statistics across all 5 runs
is output to STDERR.

## Package testing
The script `checkAccuracy.py` contains the important code to take sentences and
labels in JSON format and compare it to a spaCy model. It will then output
accuracy statistcs. You can see how it is called from within
`validateion_testing.py` and notice that the central tally of observations
(e.g., `TRAT|mislabel: 36`, `CROP|false_pos: 17`) must be cleared with
`clear_tally()` before using it again in a loop context!

You can test this code like this:
```
pytest -q test_checkAccuracy.py
```

## Manual work done initially
This required manually labeling all
entities in the 37 pages so that we could have known 'truth' labels.
This process was sped up using the Jupyter notebook `setupTraining.ipynb`
to split a page of the document into sentences, and then manual work to
yield files like `Data/barley_p1_td.py`. The output of `setupTraining.ipynb`
at the bottom of the page was cut and pasted to append to the `agData.py`
object. And this was used as input to the `setupTraning.ipynb` notebook.

### TODO item

## Next steps
There is a lot to be done, and we can divide the work. Here are some of the
items:
1. Create truth-data for additional web documents (e.g., ag experiment stations, Plant variety patents) and then assess accuracy.
2. Experiment with alternative spaCy training strategies
3. Finish recognition of JRNL and PED entries
   * Add calls to find_ped() and find_jrnl() in preparse.py as a module to the pipe
   * Remove PED and JRNL ents from the main NLP pipe
4. Finish routines that use spaCy relationships to create useful entities. E.g.
   * Add routine to handle multiple-word adjectival or adverbial modifiers like 'mid to late maturity' and 'height is very low'
   * Handle TRAT (be) ADJ constructs like 'its yield is low'
5. Create a python module to deal with compound traits using lessons learned in the CompoundTerms python notebook.
6. Clean up all the code and move academic exercises and failed experiments to an ARCHIVE folder
