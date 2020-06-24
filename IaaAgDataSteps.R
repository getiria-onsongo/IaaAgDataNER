# #### Convert single sentence data to multi-sentence data
# Davis dataset
python3 json2MultiSentence.py 3 barley_p _td.json Data/DavisLJ11  Data/DavisLJ11/parag > Data/DavisLJ11/multi_sentence.log

# CSU dataset
python3 json2MultiSentence.py 3 Bill-Brown_p _td.json Data/CSU  Data/CSU/parag > Data/CSU/bill_brown_multi_sentence.log
python3 json2MultiSentence.py 3 Cowboy_p _td.json Data/CSU  Data/CSU/parag > Data/CSU/cowboy_multi_sentence.log
python3 json2MultiSentence.py 3 Ripper_p _td.json Data/CSU  Data/CSU/parag > Data/CSU/ripper_multi_sentence.log

# UIdaho2019 dataset
python3 json2MultiSentence.py 3 small_grains_report_2019_p _td.json Data/UIdaho2019  Data/UIdaho2019/parag > Data/UIdaho2019/multi_sentence.log

# #### Create symbolic links
sh createCombineData.sh

# ### Create raw text jsonl file to use for pre-training
python3 json2rawText.py Combined_p _td.json Data/Combined Data/Combined/rawText combined_raw_text > combined_raw_text.log

# ### Pre-Train
rm -rf preTrainOutput
python3 -m spacy pretrain Data/Combined/rawText/combined_raw_text.jsonl "en_core_web_lg" preTrainOutput --use-vectors --n-iter 1000 -se 50 > pre-train.log

