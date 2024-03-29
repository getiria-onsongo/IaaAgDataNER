# NER tagging using spaCy
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
```
# Clone repository with NER training code
git clone https://github.com/getiria-onsongo/IaaAgDataNER

# Switch to the repo directory
cd IaaAgDataNER

# If you had already cloned the repo, use git pull to get the latest version. 
git pull
```

## Install spaCy 3
Install  spaCy 3 and other packages needed to annotate PDF files. 
```
pip3 install -U pip setuptools wheel
pip3 install -U spacy
pip3 install spacy-transformers
pip3 install -U scikit-learn
pip3 install -U pyxpdf

```

## Download language models
```
python3 -m spacy download en_core_web_sm
python3 -m spacy download en_core_web_md
python3 -m spacy download en_core_web_lg
```

## Generate training data
To update spaCy's model to recognize NER terms, we need training data. The folder "Data"
in this repo contains sample json files with training data. During training, spaCy 
expects two sets of data: training set and test or development set. The scripts "json2SpacyJson.py"
converts a set of json files into these two sets. NOTE, "ner_2021_08" in the command 
below will be the prefix of the output files. You can use whatever name you would like. 
The --test-size option sets size of the test set as a fraction of the total number of json
file. 0.1 means the test set will be approximately 10 percent of data in the folder "Data". 

```
python3 src/json2SpacyJson.py Data ner_2021_08 en_core_web_lg --suffix '.json' --split True --test_size 0.1

```

## Create directory to store training data in spaCy format
The program in spaCy that converts jsonl to spaCy format which is the input format for training 
models needs an output directory. 

```
mkdir ner_2021_08
```

# Convert to jsonl to spaCy binary format
```
python3 -m spacy convert --converter json ner_2021_08_training_data.jsonl ner_2021_08
python3 -m spacy convert --converter json ner_2021_08_validate_data.jsonl ner_2021_08
```

## Create config file with training parameters
Below is a description of some of the key options for creating the config file. See
spaCy for more details. 

--lang: Two-letter code of the language to use
--pipeline: Comma-separated names of trainable pipeline components to include
--optimize: Whether to optimize for efficiency or accuracy
--force: Overwrite output file if it exists
ner.cfg: name of config file


```
python3 -m spacy init config --lang en --pipeline ner  --optimize accuracy --force ner.cfg
```
NOTE: If you just have ner in the pipeline as is the case above, you will not get things such as POS which
we need. You will need to edit the resulting 
config file (ner.cfg) to include other components in the pipeline. Also, in spaCy 3, 
"attribute_ruler" is the one that creates POS. Below I am showing the fields I edited to make sure the 
resulting trained model does POS tagging. We are freezing all the components except NER from training 
because our training data is for updating NER tagging. See spaCy 3 documentation for more details. 

```
pipeline = ["tok2vec","tagger","parser","attribute_ruler","lemmatizer","ner"]

[components.tagger]
source = "en_core_web_lg"
replace_listeners = ["model.tok2vec"]

[components.parser]
source = "en_core_web_lg"
replace_listeners = ["model.tok2vec"]

[components.attribute_ruler]
source = "en_core_web_lg"
replace_listeners = ["model.tok2vec"]

[components.lemmatizer]
source = "en_core_web_lg"
replace_listeners = ["model.tok2vec"]

frozen_components = ["tagger","parser","attribute_ruler","lemmatizer"]
```

## Train model
Now that we have the config file (ner.cfg) and training data (ner_2021_08) ready, we can now train the 
english model to recognize our custom NER tags. 

```
python3 -m spacy train ner.cfg --output ner_2021_08_model --paths.train ner_2021_08/ner_2021_08_training_data.spacy --paths.dev ner_2021_08/ner_2021_08_validate_data.spacy
```

## Annotating more data using GUI
Included in this code is a graphical user interface for annotating data with custom NER tags. The GUI should 
work with both PDF and text files. It has been extensively tested on PDF files. To speed the annotation 
process, the GUI takes as one of its inputs a folder containing a model that can identify custome NER tags (output
from the training command above, ner_2021_08_model). It then pre-tags PDFs and the user can verify and correct 
pre-tagged annotations. The command below displays the GUI. 

```
# Start GUI and select "ner_2021_08_model/model-best" as the model
python3 src/CropNerGUI.py
```

## Convert new annotated data into CSV format
The GUI above will save new annotations in .json format. Users have the option of converting the annotated data 
into CSV format and loading it into a PostgreSQL database. The command below takes as input a folder (AnnotatedData)
containing NER annotations in json format and converts it into a CSV file. 

```
python3 src/json2csv.py AnnotatedData BarCvDescLJ11.csv
```

# Loading NER data into PostgreSQL
If you have access to a PostgreSQL database, the next series of steps illustrate how to load NER tagged data 
into a PostgreSQL database. 

## Create PostgreSQL
To create a database run the command below from the terminal. It will creates the database ner

```
createdb ner
```

## Create tables (relations)
Included in the code is an SQL script (CreateTables.sql) that creates tables for storing the 
9 NER tags (ALAS,CROP,CVAR,JRN,PATH,PED,PLAN,PPTD,TRAT) annoted by default. This script 
implements the schema below: 

![NER Database Schema](images/CropNer.png)


If you added your own NER tags, you might need to update this SQL script. Use this script to create tables in PostgreSQL. 


```
# hostname: would be localhost if the database is on your machine. Otherwise it is the IP address of your database. 
# ner: name of the database we created using the createdb command above. 
psql -h hostname -d ner -f src/CreateTables.sql
```

## Load Data
There is more than one way to load data into each of the tables created by the SQL script above. One way is to load data
directly from the spreadsheet into the different tables. This approach is somewhat complicated because with each load, 
you will have to tell PostgreSQL which columns to load and which ones to ignore. An easier approach, I think, would be to
create separate CSV files for each of the tables. The steps below shows how to create these separate CSV files for 
each table. 
```
# Log into PostgreSQL and load raw data (BarCvDescLJ11.csv)
psql -h hostname -d ner
\COPY raw_data FROM 'BarCvDescLJ11.csv' DELIMITER ',' CSV HEADER;

# Create CSV files for each table from raw_data
\COPY (SELECT DISTINCT crop_name FROM raw_data) to 'crop.csv' CSV;
\COPY (SELECT DISTINCT doc_name, url FROM raw_data) to 'document.csv' CSV;
\COPY (SELECT DISTINCT cvar, crop_name FROM raw_data) to 'crop_variety.csv' CSV;
\COPY (SELECT DISTINCT id, chunk, doc_name, cvar FROM raw_data) to 'cvar_data_source.csv' CSV;
\COPY (SELECT DISTINCT id, label FROM raw_data) to 'ner_tag.csv' CSV;
\COPY (SELECT DISTINCT value, id, label FROM raw_data) to 'crop_attribute.csv' CSV;

# Load data to tables
\COPY crop FROM 'crop.csv' DELIMITER ',' QUOTE '"' CSV;
\COPY document FROM 'document.csv' DELIMITER ',' QUOTE '"' CSV;
\COPY crop_variety FROM 'crop_variety.csv' DELIMITER ',' QUOTE '"' CSV;
\COPY cvar_data_source FROM 'cvar_data_source.csv' DELIMITER ',' QUOTE '"' CSV;
\COPY ner_tag FROM 'ner_tag.csv' DELIMITER ',' QUOTE '"' CSV;
\COPY crop_attribute FROM 'crop_attribute.csv' DELIMITER ',' QUOTE '"' CSV;

```

## Do some basic optimization
The schema above is good for reducing data duplication in the database. It is, however, not 
suitable for the kind of queries a typical user might be interested in. The commands below
create a view that aggregates data into a view that is easier to query. NOTE: If performance 
becomes an issue, we will need to use materialized views instead of plain views. 

```
# Log into PostgreSQL 
psql -h hostname -d ner

# Create indexes to speed up query that creates the view. As noted, if queries against 
# views start slowing down, transition to materialized views. 
CREATE INDEX crop_attribute_id_idx ON crop_attribute USING BTREE(id);

# Create view
CREATE VIEW crop_data AS
SELECT DISTINCT crop_name, cvar, label, value FROM
(SELECT crop_name, cvar, id FROM crop_variety JOIN cvar_data_source USING(cvar)) A
JOIN
crop_attribute B
USING(ID);

```

## Sample Query
Try a sample query. This query is a back-end SQL implementation that will serve one the sample API calls in the [Crop Trait Explorer](https://docs.google.com/document/d/1nb6cxjrVUWXbs-tpyjO7WLdkQyHqd-CjnGhY5NPkYJc/edit?usp=sharing) document. 

```
# Log into PostgreSQL 
psql -h hostname -d ner

# Create indexes to speed up query that creates the view. As noted, if queries against 
# views start slowing down, transition to materialized views. 
CREATE INDEX crop_attribute_id_idx ON crop_attribute USING BTREE(id);

# Create view
CREATE VIEW crop_data AS
SELECT DISTINCT crop_name, cvar, label, value FROM
(SELECT crop_name, cvar, id FROM crop_variety JOIN cvar_data_source USING(cvar)) A
JOIN
crop_attribute B
USING(ID);

```


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
