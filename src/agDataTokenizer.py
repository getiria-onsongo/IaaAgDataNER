from spacy.gold import biluo_tags_from_offsets
import spacy
import srsly
from spacy.gold import docs_to_json
import json
import PyPDF2

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
        tokens = []
        cnt = 0
        for sent in doc.sents:
            doc2 = nlp(sent.text)
            for token in doc2:
                tokens.append(token.text)
            if(cnt > 5):
                data.append({"tokens": tokens})
                tokens = []
                cnt = 0
            cnt = cnt + 1

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

def nerDataToJSON(data, fileName,nlp):
    ''' Take as input ner training data and convert it into
    CLI json training data.'''
    # nlp = spacy.load('en_core_web_lg')
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
            docs_dict['paragraphs'][0]['sentences'][0]['tokens'][i]['ner'] = tags[i]
        if(cnt > 0):
            file.write(",")
            file.write("\n")
        file.write(json.dumps(docs_dict))

        cnt = cnt + 1
    file.write("]")
    file.close()

# python3 -m spacy download en_core_web_lg
nlp = spacy.load('en_core_web_lg')

# Generate raw text for training
# rm -rf Data/DavisLJ11/rawText
# mkdir -p Data/DavisLJ11/rawText
# python3 json2rawText.py 3 barley_p _td.json Data/DavisLJ11  Data/DavisLJ11/rawText DavisLJ11_raw_text

## ADD STEPS TO GENERATE trainData.json AND devData.json
# To validate training data. NOTE: I have observed this validation fails if we use a custom
# tokenizer. Pre-train and train still works even with a failed data debug. Just an FYI
# python3 -m spacy debug-data en trainData.json devData.json -b "en_core_web_lg" -p ner -V

# rm -rf preTrainOutput
# python3 -m spacy pretrain Data/DavisLJ11/rawText/DavisLJ11_raw_text.jsonl "en_core_web_lg" preTrainOutput --use-vectors --n-iter 1000 -se 50

# To find out more about commands
# > python3 -m spacy train -h

# NOTE: If you get an error along the line of "TypeError: '>' not supported between instances of 'dict' and 'dict'"
# here is the fix: https://github.com/explosion/spaCy/pull/5186/files
# The file will probably be at this location: /usr/local/lib/python3.7/site-packages/spacy/cli/train.py
# You will need to add 5 lines in: train.py

# rm -rf NerModelPreTrain
# python3 -m spacy train en NerModelPreTrain trainData.json devData.json --init-tok2vec preTrainOutput/model999.bin --vectors "en_core_web_lg" --pipeline ner --n-iter 1000 --n-early-stopping 10  --debug

# Train without pre-training
# rm -rf NerModel
# python3 -m spacy train en NerModel trainData.json devData.json --vectors "en_core_web_lg" --pipeline ner --n-iter 1000 --n-early-stopping 10  --debug


# Not sure why training is not working with --raw-text
# python3 -m spacy train en NerModelPreTrain trainData.json devData.json --init-tok2vec preTrainOutput/model999.bin --vectors "en_core_web_lg" --pipeline ner --n-iter 1000 --n-early-stopping 10 --raw-text Data/DavisLJ11/rawText/DavisLJ11_raw_text.jsonl --debug

# Understanding training output: see https://spacy.io/usage/training

# NER Loss: Training loss for named entity recognizer. Should decrease, but usually not to 0.
# NER P: NER precision on development data. Should increase.
# NER R: NER recall on development data. Should increase.
# NER F: NER F-score on development data. Should increase.





# MISC
# NEXT WE NEED TO GO THROUGH AND UPDATE NER TAGS
# NOTE: BE SURE TO USE THE SAME NLP (SAME TOKENIZER)

# --use-vectors to use the vectors from existing English model.


# rm -rf NerModel

# python3 -m spacy train en --base-mode "en_core_web_lg" NerModel trainData.json devData.json --pipeline ner --init-tok2ve preTrainOutput/model9.bin --n-iter 10


# Change --n-iter 1000 in actual implementation


# python3 -m spacy train en NerModel trainData.json devData.json -p ner -v "en_core_web_lg" -t2v preTrainOutput/model999.bin -n 30 -ne 5 -D

# python3 -m spacy convert trainData.json --converter jsonl -l en > trainData.jsonl

#data = [{"text": "It was selected from the cross I1162-19/J-126//WA1245///Steptoe"}, {"text": "Its experimental designation was 79Ab812."}]
#srsly.write_jsonl("raw.jsonl", data)