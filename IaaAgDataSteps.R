# #### Create symbolic links
sh createCombineDataSingleSentence.sh

# ### Create raw text jsonl file to use for pre-training
python3 json2rawText.py Combined_p _td.json Data/CombinedSingleSentence Data/CombinedSingleSentence combined_raw_text > Data/CombinedSingleSentence/combined_raw_text.log

# ### Pre-Train
rm -rf preTrainOutput
python3 -m spacy pretrain Data/CombinedSingleSentence/combined_raw_text.jsonl  "en_core_web_md" preTrainOutput --use-vectors --n-iter 1000 -se 100


# ### Test models
# I prefer this testing option for now because the datasets are imbalanced. Better performance of barley datasets which is
# about 50% of the pages will mask bad performance of CSU abd Idaho datasets.

python3 -m spacy debug-data en UIdaho_test_pretrain_cli_training_data.json UIdaho_test_pretrain_cli_validate_data.json -b en_core_web_md -p ner -V

mkdir -p CSU_test_35
python3 ner_model_testing.py 35 '4,7' 'Combined_p' '_td.json' Data/CombinedSingleSentence CSU_test_35 CSU_test

mkdir -p CSU_pretrain_test_35
python3 ner_model_testing_cli.py 35 '4,7' 'Combined_p' '_td.json' Data/CombinedSingleSentence CSU_pretrain_test_35 CSU_test_pretrain preTrainOutput/model999.bin

mkdir -p CSU_test_54
python3 ner_model_testing.py 54 '4,7' 'Combined_p' '_td.json' Data/CombinedSingleSentence CSU_test_54 CSU_test

mkdir -p CSU_pretrain_test_54
python3 ner_model_testing_cli.py 54 '4,7' 'Combined_p' '_td.json' Data/CombinedSingleSentence CSU_pretrain_test_54 CSU_test_pretrain preTrainOutput/model999.bin

mkdir -p UIdaho_test_35
python3 ner_model_testing.py 35 '11,14' 'Combined_p' '_td.json' Data/CombinedSingleSentence UIdaho_test_35 UIdaho_test

mkdir -p UIdaho_pretrain_test_35
python3 ner_model_testing_cli.py 35 '11,14' 'Combined_p' '_td.json' Data/CombinedSingleSentence UIdaho_pretrain_test_35 UIdaho_test_pretrain preTrainOutput/model999.bin

mkdir -p UIdaho_test_54
python3 ner_model_testing.py 54 '11,14' 'Combined_p' '_td.json' Data/CombinedSingleSentence UIdaho_test_54 UIdaho_test

mkdir -p UIdaho_pretrain_test_54
python3 ner_model_testing_cli.py 54 '11,14' 'Combined_p' '_td.json' Data/CombinedSingleSentence UIdaho_pretrain_test_54 UIdaho_test_pretrain preTrainOutput/model999.bin

mkdir -p DavisLJ11_test_35
# NOTE: Pages in test dataset have to be between 1 and maxn
python3 ner_model_testing.py 35 '19,24,27' 'Combined_p' '_td.json' Data/CombinedSingleSentence DavisLJ11_test_35 DavisLJ11_test

mkdir -p DavisLJ11_pretrain_test_35
python3 ner_model_testing_cli.py 35 '19,24,27' 'Combined_p' '_td.json' Data/CombinedSingleSentence DavisLJ11_pretrain_test_35 DavisLJ11_test_pretrain preTrainOutput/model999.bin

mkdir -p DavisLJ11_test_54
python3 ner_model_testing.py 54 '19,24,27' 'Combined_p' '_td.json' Data/CombinedSingleSentence DavisLJ11_test_54 DavisLJ11_test

mkdir -p DavisLJ11_pretrain_test_54
python3 ner_model_testing_cli.py 54 '19,24,27' 'Combined_p' '_td.json' Data/CombinedSingleSentence DavisLJ11_pretrain_test_54 DavisLJ11_test_pretrain preTrainOutput/model999.bin














# ### Leave one out cross validation
# Use the leave one out cross validation when we have a more balanced dataset.
mkdir -p CombinedNoPreTrain
python3 validation_testing.py 35 'Combined_p' '_td.json' Data/CombinedSingleSentence CombinedNoPreTrain 'CombinedNoPreTrain_'

mkdir -p CombinedNoPreTrainAllData
python3 validation_testing.py 54 'Combined_p' '_td.json' Data/CombinedSingleSentence CombinedNoPreTrainAllData 'CombinedNoPreTrain_'






# python3 validation_testing_pretrain.py 3 barley_p _td.json temp temp_out temp preTrainOutput/model999.bin






# MISC
# #### Convert single sentence data to multi-sentence data
# Davis dataset
python3 json2MultiSentence.py 3 barley_p _td.json Data/DavisLJ11  Data/DavisLJ11/parag > Data/DavisLJ11/multi_sentence.log

# CSU dataset
python3 json2MultiSentence.py 3 Bill-Brown_p _td.json Data/CSU  Data/CSU/parag > Data/CSU/bill_brown_multi_sentence.log
python3 json2MultiSentence.py 3 Cowboy_p _td.json Data/CSU  Data/CSU/parag > Data/CSU/cowboy_multi_sentence.log
python3 json2MultiSentence.py 3 Ripper_p _td.json Data/CSU  Data/CSU/parag > Data/CSU/ripper_multi_sentence.log

# UIdaho2019 dataset
python3 json2MultiSentence.py 3 small_grains_report_2019_p _td.json Data/UIdaho2019  Data/UIdaho2019/parag > Data/UIdaho2019/multi_sentence.log

