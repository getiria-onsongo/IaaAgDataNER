#!/bin/env python3

from validation_testing_pretrain import *
import subprocess
import spacy

def execute(cmd):
    """
        Takes as input a command to execute (cmd: str), executes the command and
        returns the exit code (exit_code)
    """

    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout_data, stderr_data) = process.communicate()
    return_code = process.wait()

    if (return_code != 0):
        print("Error:", stderr_data)
        raise ValueError("Failed to execute command:", cmd)

    sys.stderr.write(stderr_data.decode())
    sys.stdout.write(stdout_data.decode())
    return return_code

maxn = 2
fprefix= "barley_p"
input_dir= "temp"
fsuffix = "_td.json"
output_dir = "temp_out"
output_prefix = "barley"
preTrain = "preTrainOutput/model999.bin"
n_iter=10
early_stop = 2
for i in range(1, maxn+1):
    trainFile_name=build_nth_dataset(i, maxn, "barley_p", "_td.json", "temp", "temp_out", "barley")
    test_file = input_dir+"/"+fprefix+str(i)+fsuffix

    training_data_file_name = output_dir + "/" + output_prefix + str(i) + "_training_data.json"
    validate_data_file_name = output_dir + "/" + output_prefix + str(i) + "_validate_data.json"
    test_size = 0.1
    convert_to_biluo_tags(trainFile_name, test_size, training_data_file_name,validate_data_file_name)

    validate_cmd =  "python3 -m spacy debug-data en "+training_data_file_name+" "+validate_data_file_name+ " -b \"en_core_web_lg\" -p ner -V"
    print(validate_cmd)
    result=execute(validate_cmd)

    # model_dir = train_nth_model(i, output_dir+"/"+output_prefix+str(i)+".json", output_dir, output_prefix)
    model_dir = output_dir + "/" + output_prefix + "_model_"+str(i)
    train_cmd = "python3 -m spacy train en " + model_dir + " " + training_data_file_name + " " + validate_data_file_name + " --init-tok2vec " + preTrain + "  --vectors \"en_core_web_lg\" --pipeline ner --n-iter "+str(n_iter)+" --n-early-stopping "+str(early_stop)+"  --debug"
    print(train_cmd)
    result = execute(train_cmd)

    trained_model = model_dir+"/model-best"
    agdata_nlp = spacy.load(trained_model)

    doc = agdata_nlp("It was selected from the cross Steveland/Luther//Wintermalt")
    for token in doc:
        print(token.text)



    #
    #train_cmd = "python3 -m spacy train en "+model_dir+" "+training_data_file_name+" "+test_data_file_name+" --init-tok2vec"+preTrain+"  --vectors \"en_core_web_lg\" --pipeline ner --n-iter 1000 --n-early-stopping 10  --debug"
