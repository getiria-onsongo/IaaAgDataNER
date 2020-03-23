from spacy.lang.char_classes import ALPHA, ALPHA_LOWER, ALPHA_UPPER,CONCAT_QUOTES, LIST_ELLIPSES, LIST_ICONS
from spacy.util import compile_infix_regex
from spacy.gold import biluo_tags_from_offsets
import re
import spacy
from spacy.matcher import Matcher
import srsly
from spacy.util import minibatch, compounding
from agData import *
import random
from pathlib import Path
from spacy.gold import docs_to_json
import json
import PyPDF2

DEV_DATA = [
    ('Eight-Twelve is a six-rowed winter feed barley.', {'entities': [(0, 12, 'CVAR'), (18, 27, 'TRAT'), (28, 34, 'TRAT'), (35, 39, 'CVAR'), (40, 46, 'CROP')]}),
    ('It was released by the USDA-ARS and the Idaho AES in 1991.', {'entities': [(23, 31, 'ORG'), (40, 49, 'ORG'), (53, 57, 'DATE')]}),
    ('It was selected from the cross Steveland/Luther//Wintermalt.', {'entities': [(31, 59, 'PED')]}),
    ('Its experimental designation was 79Ab812.', {'entities': [(33, 40, 'ALAS')]})]

path_to_pretrained_weights="/Users/gonsongo/Desktop/research/iaa/Projects/python/IaaAgDataNER/preTrainInput/text.jsonl"

def trainModel(model=None, output_dir=None, n_iter=100):
    """Load the model, set up the pipeline and train the entity recognizer."""
    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Model loaded.. '%s'" % model)
    else:
        nlp = spacy.blank("en_core_web_lg")  # create blank Language class
        print("Created blank 'en_core_web_lg' model")

    # create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe(ner, last=True)
    # otherwise, get it so we can add labels
    else:
        ner = nlp.get_pipe("ner")

    # add entity labels
    for _, annotations in TRAIN_DATA:
        for ent in annotations.get("entities"):

            ner.add_label(ent[2])

    # get names of other pipes to disable them during training, if present
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]



    with nlp.disable_pipes(*other_pipes):  # only train NER
        # reset and initialize the weights randomly – but only if we're
        # training a new model
        if model is None:
            nlp.begin_training()

            # Now that we have our model, we can load in the pretrained weights.
            with open(path_to_pretrained_weights, "rb") as file_:
                nlp.model.tok2vec.from_bytes(file_.read())

        q1 = int(n_iter // 4)
        q2 = int(q1 * 2)
        q3 = int(q1 * 3)

        for itn in range(n_iter):
            if itn == q1:
                print("Training 25% done")
            elif itn == q2:
                print("Training 50% done")
            elif itn == q3:
                print("Training 75% done")
            random.shuffle(TRAIN_DATA)
            losses = {}
            # batch up the examples using spaCy's minibatch
            batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(
                    texts,  # batch of texts
                    annotations,  # batch of annotations
                    drop=0.5,  # dropout - make it harder to memorise data
                    losses=losses,
                )
            # print("Losses", losses)

    print("Training complete!")
    # save model to output directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)



# The code below is custom to agData. It modifies how the
# parser works to avoid splitting pedigrees

nlp = spacy.load('en_core_web_lg')

# Tell spacy not to split between hyphens
infixes = (
        LIST_ELLIPSES
        + LIST_ICONS
        + [
            #r"(?<=[0-9])[+\-\*^](?=[0-9-])",
            r"(?<=[0-9])[+\*^](?=[0-9-])", # Do not split on -
            r"(?<=[{al}{q}])\.(?=[{au}{q}])".format(
                al=ALPHA_LOWER, au=ALPHA_UPPER, q=CONCAT_QUOTES),
            r"(?<=[{a}]),(?=[{a}])".format(a=ALPHA),
            r"(?<=[{a}0-9])[:<>=](?=[{a}])".format(a=ALPHA) # Do not split in /
           #r"(?<=[{a}0-9])[:<>=/](?=[{a}])".format(a=ALPHA)
        ]
        )
infix_re = compile_infix_regex(infixes)
# Tell spacy not to split between hyphens (-) and slashes (/)
nlp.tokenizer.infix_finditer = infix_re.finditer

# Try to match journal: Crop Science 32(3):828 (1992)
digit_hyphen_re = re.compile(r'\s\(\d\)')
nlp.tokenizer.token_match = digit_hyphen_re.search

def pdfToJSON(inputPDF, outputFilename, nlp):
    pdfFile = open(inputPDF, mode="rb")
    data = []
    pdfReader = PyPDF2.PdfFileReader(pdfFile)
    numPages = pdfReader.getNumPages()
    for i in range(numPages):
        OnePage = pdfReader.getPage(i)
        OnePageText = OnePage.extractText()
        OnePageText = OnePageText.replace('\n', '')
        doc = nlp(OnePageText)
        for sent in doc.sents:
            data.append({"text":sent.text})

    srsly.write_jsonl(outputFilename, data)
    pdfFile.close()

def pdfToTokensJSON(inputPDF, outputFilename, nlp):
    pdfFile = open(inputPDF, mode="rb")
    data = []
    pdfReader = PyPDF2.PdfFileReader(pdfFile)
    numPages = pdfReader.getNumPages()
    for i in range(numPages):
        OnePage = pdfReader.getPage(i)
        OnePageText = OnePage.extractText()
        OnePageText = OnePageText.replace('\n', '')
        doc = nlp(OnePageText)
        for sent in doc.sents:
            tokens = []
            doc2 = nlp(sent.text)
            for token in doc2:
                tokens.append(token.text)
            data.append({"tokens":tokens})

    srsly.write_jsonl(outputFilename, data)
    pdfFile.close()


def entitiesToJSON(fileName, data):
    file = open(fileName, "w")
    for entry in data:
        trainDataJson = {}
        ents = []
        entities = entry[1]['entities']
        for ent in entities:
            entData = {}
            entData['start'] = ent[0]
            entData['end'] = ent[1]
            entData['label'] = ent[2]
            ents.append(entData)
        trainDataJson['text'] = entry[0]
        trainDataJson['spans'] = ents
        file.write(json.dumps(trainDataJson))
        file.write("\n")
    file.close()

def nerDataToJSON(nlp, data, fileName):
    ''' Take as input ner training data and convert it into
    CLI json training data.'''
    file = open(fileName, "w")
    file.write("[")
    cnt = 0
    for entry in data:
        rawText = entry[0]
        doc = nlp(rawText)
        entities = entry[1]['entities']
        tags = biluo_tags_from_offsets(doc, entities)
        docs_dict = docs_to_json([doc], cnt)
        for i in range(len(docs_dict['paragraphs'][0]['sentences'][0]['tokens'])):
            # I added the if statement because the following NER example is not being tagged correctly
            # ('Maja is a six-rowed winter feed/malt barley.', {'entities': [(0, 4, 'CVAR'), (10, 19, 'TRAT'), (20, 26, 'TRAT'), (27, 31, 'TRAT'), (32, 36, 'TRAT'), (37, 43, 'CROP')]}),
            if (tags[i] == '-'):
                docs_dict['paragraphs'][0]['sentences'][0]['tokens'][i]['ner'] = 'O'
            else:
                docs_dict['paragraphs'][0]['sentences'][0]['tokens'][i]['ner'] = tags[i]
        if(cnt > 0):
            file.write(",")
            file.write("\n")
        file.write(json.dumps(docs_dict))

        cnt = cnt + 1
    file.write("]")
    file.close()

'''
doc = nlp("It was selected from the cross Steveland/Luther//Wintermalt")
for token in doc:
    print(token.text)
'''
# TO DO
# 1) FINALIZE AND TEST TOKENIZER
# 2) CREATE PRE-TRAINING DATA. AT THE MOMENT I CAN ONLY GET IT TO WORK WITH
# ONE DICTIONARY WITH A SINGLE KEY (TOKENS)
'''
doc = nlp("It was derived from I1162-19/J-126//WA1245///Steptoe.")
values=[]
for token in doc:
    values.append(token.text)
preTrainData=[{"tokens":values}]
path="/Users/gonsongo/Desktop/research/iaa/Projects/python/IaaAgDataNER/preTrainInput"
srsly.write_jsonl(path+"/text.jsonl", preTrainData)

entitiesToJSON("devData.json", DEV_DATA)
x = TRAIN_DATA[0:10]
entitiesToJSON("trainData.json", x)
#print("len(x)=",len(x))


 
doc = nlp("It was selected from the cross I1162-19/J-126//WA1245///Steptoe")
for token in doc:
    print(token.text)


doc = nlp("The journal is Crop Science 32(3):828 (1992)")

# for token in doc:
#     print(token.text)

# CODE FOR FIXING JOURNAL TOKENS
indexes = [m.span() for m in re.finditer('[\w|\S]+\s[\w|\S]+\s\([\w|\S]+\)', doc.text, flags=re.IGNORECASE)]
print("\n")
print(indexes)
for (span_start, span_end) in indexes:
    print(doc.text[span_start:span_end])
'''

#
'''
t1 = "Eight-Twelve is a six-rowed winter feed barley."
t2 = "New York was derived in Great Britain from I1162-19/J-126//WA1245///Steptoe."
t = [t1, t2]
file = open("testOne.json", "w")
file.write("[")
#print("len(t)=",len(t))
for i in range(len(t)):
    doc = nlp(t[i])
    json_data = docs_to_json([doc],i)
    file.write(json.dumps(json_data))

    for ent in doc.ents:
        print(ent.text + ' - ' + ent.label_ + ' - ' + str(spacy.explain(ent.label_)))
file.write("]")
file.close()
'''
#('It was selected from the cross Steveland/Luther//Wintermalt.', {'entities': [(31, 59, 'PED')]}),

#doc = nlp.pipe("It was selected from the cross Steveland/Luther//Wintermalt.", disable=["tagger", "parser"])
'''
doc1 = nlp("It was selected from the cross Steveland/Luther//Wintermalt.")
entities = [(31, 59, 'PED')]
tags = biluo_tags_from_offsets(doc1, entities)
print("tags=", tags)
print(docs_to_json([doc1]))


# ('Eight-Twelve is a six-rowed winter feed barley.', {'entities': [(0, 12, 'CVAR'), (18, 27, 'TRAT'), (28, 34, 'TRAT'), (35, 39, 'CVAR'), (40, 46, 'CROP')]})
print("\n\n")
doc2 = nlp("Eight-Twelve is a six-rowed winter feed barley.")
entities = [(0, 12, 'CVAR'), (18, 27, 'TRAT'), (28, 34, 'TRAT'), (35, 39, 'CVAR'), (40, 46, 'CROP')]
tags = biluo_tags_from_offsets(doc2, entities)
print("tags=", tags)
print(docs_to_json([doc2]))

# ('Its experimental designation was 79Ab812.', {'entities': [(33, 40, 'ALAS')]})]
# ('Maja is a six-rowed winter feed/malt barley.', {'entities': [(0, 4, 'CVAR'), (10, 19, 'TRAT'), (20, 26, 'TRAT'), (27, 31, 'TRAT'), (32, 36, 'TRAT'), (37, 43, 'CROP')]}),
# ('It is medium height (2 inches shorter than Steptoe) and has moderately stiff straw.', {'entities': [(13, 19, 'TRAT'), (43, 50, 'CVAR'), (77, 82, 'PLAN')]}),
#

print("\n\n")
doc3 = nlp("It was selected from the cross Luther/Hudson//Alpine/Svalof//White Winter/Triple Bearded Mariout-305.")
entities = [(31, 100, 'PED')]
tags = biluo_tags_from_offsets(doc3, entities)
print("tags=", tags)
docs_dict = docs_to_json([doc3])

print("Before")
print(docs_dict)

#print(type(docs_to_json([doc3])))


for i in range(len(docs_dict['paragraphs'][0]['sentences'][0]['tokens'])):
    docs_dict['paragraphs'][0]['sentences'][0]['tokens'][i]['ner'] = tags[i]
    #print(docs_dict['paragraphs'][0]['sentences'][0]['tokens'][i])

print("After")
print(docs_dict)
'''
buggyEntries = [TRAIN_DATA[29],TRAIN_DATA[61],TRAIN_DATA[66],TRAIN_DATA[181],TRAIN_DATA[197]
                ,TRAIN_DATA[211],TRAIN_DATA[219],TRAIN_DATA[231],TRAIN_DATA[253],TRAIN_DATA[257],
                TRAIN_DATA[276],TRAIN_DATA[280],TRAIN_DATA[282],TRAIN_DATA[340],TRAIN_DATA[447],
                TRAIN_DATA[505],TRAIN_DATA[575],TRAIN_DATA[664]]

x = TRAIN_DATA[0:29]
x.extend(TRAIN_DATA[30:61])
x.extend(TRAIN_DATA[62:66])
x.extend(TRAIN_DATA[67:181])
x.extend(TRAIN_DATA[182:197])
x.extend(TRAIN_DATA[198:211])
x.extend(TRAIN_DATA[212:219])
x.extend(TRAIN_DATA[220:231])
x.extend(TRAIN_DATA[232:253])
x.extend(TRAIN_DATA[254:257])
x.extend(TRAIN_DATA[258:276])
x.extend(TRAIN_DATA[277:280])
x.extend(TRAIN_DATA[281:282])
x.extend(TRAIN_DATA[283:340])
x.extend(TRAIN_DATA[341:447])
x.extend(TRAIN_DATA[448:505])
x.extend(TRAIN_DATA[506:575])
x.extend(TRAIN_DATA[576:664])
x.extend(TRAIN_DATA[665:])
pdfToJSON("BarCvDescLJ11.pdf", "raw.json", nlp)
nerDataToJSON(nlp,x[0:50],"devData.json")
nerDataToJSON(nlp,x[50:],"trainData.json")

pdfToTokensJSON("BarCvDescLJ11.pdf", "rawTokens.json", nlp)
pdfToJSON("BarCvDescLJ11.pdf", "raw.json", nlp)

# python3 -m spacy download en_core_web_lg

# To validate training data
# python3 -m spacy debug-data en trainData.json devData.json -b "en_core_web_lg" -p ner -V

# rm -rf preTrainOutput

# python3 -m spacy pretrain rawTokens.json "en_core_web_lg" preTrainOutput --use-vectors --n-iter 1000 -se 10

# rm -rf NerModel

# python3 -m spacy train en NerModel trainData.json devData.json -t2v preTrainOutput/model999.bin -v "en_core_web_lg" -p ner -n 50 -ne 5 -rt raw.json -D

# -- HERE

# python3 -m spacy train en NerModel trainData.json devData.json -p ner -v "en_core_web_lg" -t2v preTrainOutput/model999.bin -n 30 -ne 5 -D

# -- HERE

# NEXT WE NEED TO GO THROUGH AN UPDATE NER TAGS
# NOTE: BE SURE TO USE THE SAME NLP (SAME TOKENIZER)

# --use-vectors to use the vectors from existing English model.


# rm -rf NerModel

# python3 -m spacy train en --base-mode "en_core_web_lg" NerModel trainData.json devData.json --pipeline ner --init-tok2ve preTrainOutput/model9.bin --n-iter 10


# Change --n-iter 1000 in actual implementation

# MISC
# python3 -m spacy convert trainData.json --converter jsonl -l en > trainData.jsonl

#data = [{"text": "It was selected from the cross I1162-19/J-126//WA1245///Steptoe"}, {"text": "Its experimental designation was 79Ab812."}]
#srsly.write_jsonl("raw.jsonl", data)