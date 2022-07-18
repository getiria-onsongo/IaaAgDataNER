python3 src/json2SpacyJson.py Data/page_level ner_2021_08 en_core_web_lg --suffix '.json' --split True --test_size 0.1
mkdir ner_2021_08
python3 -m spacy convert --converter json ner_2021_08_training_data.jsonl ner_2021_08
python3 -m spacy convert --converter json ner_2021_08_validate_data.jsonl ner_2021_08
python3 -m spacy init config --lang en --pipeline tok2vec,senter,ner  --optimize accuracy --force senter_ner.cfg
python3 -m spacy init vectors en glove.6B.zip senter_ner_2021_08_model
python3 -m spacy train senter_ner.cfg --output senter_ner_2021_08_model --paths.train ner_2021_08/ner_2021_08_training_data.spacy --paths.dev ner_2021_08/ner_2021_08_validate_data.spacy
