# IaaAgDataNER
Parse and categorize agricultural related data

## Background
The approach we will use for NER tagging is to take the existing spaCy English language
model build on it to recognize agricultural specific NER terms. We are currently working 
on training it to  recognize the following terms: 
- ALAS = varietal alias
- CROP = crop
- CVAR = crop_variety
- JRNL = journal reference
- PATH = pathogen
- PED  = pedigree
- PLAN = plant anatomy
- PPTD = plant predisposition to disease
- TRAT = trait

<!---
We are starting out by training the NER on the 37 pages of
[BarCvDescLJ11.pdf](https://smallgrains.ucdavis.edu/cereal_files/BarCvDescLJ11.pdf),
a compendium of barley varieties.


## Getting started
You can test the accuracy of the NER training with N pages of the 37 page document. However, our experience with SpaCy training so far is it converges faster if you use more data. If you have a total of maxn pages, it is a good idea to use all the pages. 

We wrote a script that does leave-one-out cross validation. Because training an NER model is time consuming, we do not recommend performing the full leave-one-out cross validation when testing. If you have a total on N pages, the NER model will be trained N times. Test the script without the --validate flag. If this flag is ommitted, the analysis will be done once. One of the pages will be randomly selected to be the test page. The remaining pages will be used for training. Check for yourself!
-->

## Clone repository
Before you start, make sure you have Python3 installed. If you are reading this README file it means you 
have cloned this repository. If not, clone this repo using the steps shown below. 


<!---
```
# Clone repository with NER training code
git clone https://github.com/getiria-onsongo/IaaAgDataNER

cd IaaAgDataNER

mkdir /tmp/spacy

# To send output to a file (test_results.txt) instead of STDERR
python3 src/validation_testing.py 37 'barley_p' '_td.json' Data/DavisLJ11  /tmp/spacy 'test_' 2> test_results.txt

# To send output to STDERR
python3 src/validation_testing.py 37 'barley_p' '_td.json' Data/DavisLJ11  /tmp/spacy 'test_'

```
This will randomly pick one of the pages (range 1 - 37) and set it aside as the test page. It
will then use the remaining pages to train the NER model and test its performance on the test page. 
Training accuracy stats are computed and sent to STDERR or to a file (test_results.txt) if one 
is specified. 

## Leave-one-out cross validation
If you want to perform leave-one-out cross validation, execute the command above with the --validate flag. 
NOTE: This will likely take a long time. We recommend testing the script without the --validate flag to
determine how long a single training takes. If you have N pages, estimate the total running time before 
you perform the actual cross-validation. Chances are you will need to run this overnight if you are using a
machine with 4 or fewer cores. 

```
python3 src/validation_testing.py 37 'barley_p' '_td.json' Data/DavisLJ11  /tmp/spacy 'test_' --validate 2> test_results.txt
```
This will generate 37 training files in `/tmp/spacy`: one that has
pages 2-37, one with page 1 and 3-37, one with pages 1-2 and 4-37, etc. A
model is created for each, and training accuracy stats are computed
for each one as well. Finally a compilation of statistics across all 37 runs
is output to STDERR.

## Package testing
The script `checkAccuracy.py` contains the important code to take sentences and
labels in JSON format and compare it to a spaCy model. It will then output
accuracy statistcs. You can see how it is called from within
`validation_testing.py` and notice that the central tally of observations
(e.g., `TRAT|mislabel: 36`, `CROP|false_pos: 17`) must be cleared with
`clear_tally()` before using it again in a loop context!

This code uses pytest. You need to have the module pytest installed. You will need
to have an NER model trained e.g., /tmp/spacy/model-best. Open src/test_checkAccuracy.py
and update mdir to point to your model i.e., mdir = "/tmp/spacy/model-best"

You can then test this code like this:
```
cd src
python -m pytest -q test_checkAccuracy.py
```
NOTE: As of Feb 12 2021, the move to Spacy 3.0 resulted in 2 of the tests failing. If 
you are seeing this note it means that issue has not been resolved. Need to chat with @kats
who wrote the tests to figure out what the issue is. 

## Trying things out
If you wish to play with it on the interpreter line, try this:
```

from src.agParse import *

text = 'Kold is a six-rowed winter feed barley obtained from the cross Triumph/Victor. It was released by the Oregon AES in 1993. It has rough awns and the aleurone is white. It has low lodging, matures early and its yield is low. Crop Science 25:1123 (1985).'

# Set up the pipeline
source_nlp = spacy.load("en_core_web_sm")
nlp = spacy.load('NerModel/model-best')
nlp.add_pipe("parser", before="ner",source=source_nlp)
nlp.add_pipe("tagger", before="parser",source=source_nlp)

# Show components in pipeline
nlp.pipe_names

doc = nlp(text)
for ent in doc.ents:
    print(ent.text, ent.start_char, ent.end_char, ent.label_)
```

## Manual work done initially
This required manually labeling all
entities in the 37 pages so that we could have known 'truth' labels.
This process was sped up using the Jupyter notebook `CreatingTrainingData.ipynb`
to split a page of the document into sentences, and then manual work to
yield files like `Data/barley_p1_td.py`. The output of `CreatingTrainingData.ipynb`
at the bottom of the page was cut and pasted to append to the `agData.py`
object. 

### TODO item

## Next steps
There is a lot to be done, and we can divide the work. Here are some of the
items:
1. Create truth-data for additional web documents (e.g., ag experiment stations, Plant variety patents) and then assess accuracy.
2. Experiment with alternative spaCy training strategies
3. Finish routines that use spaCy relationships to create useful entities. E.g.
   * Add routine to handle multiple-word adjectival or adverbial modifiers like 'mid to late maturity' and 'height is very low'
   * Handle TRAT (be) ADJ constructs like 'its yield is low'
4. Create a python module to deal with compound traits using lessons learned in the CompoundTerms python notebook.
5. Clean up all the code and move academic exercises and failed experiments to an ARCHIVE folder
-->
