import os
import subprocess
import json
import threading
from glob import glob

#/home/rabee/thesis/master_thesis_rabee_sohail/data_extraction/data/js_temp
threadLock = threading.Lock()
output_file_index = 0
num_funcs = 0
num_files = 0


def invoke(config):
    files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(config['input_dir']) for f in filenames]


    funcs = []
    print "number of files is: ", len(files)
    command = "jsdoc -X "
    num_funcs = 0
    count = 0
    for index, file in enumerate(files):
        try:
            output = subprocess.check_output(command + file, shell=True)
            funcs_json = to_valid_json(output)
            if index % 10 == 0:
                print "Processed files {}".format(index)
            for index, func_json in enumerate(funcs_json):
                if "kind" in func_json and func_json["kind"] == "function":
                    funcs.append(func_json)

            if len(funcs) > 10000:
                count += 1
                write_funcs_to_file(funcs, count, config['output_dir'])
                num_funcs += len(funcs)
                funcs = []
        except subprocess.CalledProcessError:
            print "Skipped a file!"

    count += 1
    write_funcs_to_file(funcs, count, config['output_dir'])
    num_funcs += len(funcs)

    print "the total number of functions processed is: {}".format(num_funcs)


def to_valid_json(jsonString):
    try:
        return json.loads(jsonString)
    except ValueError:
        return ""


def write_funcs_to_file(funcs, index, output_dir):
    out_file_name = "jsdoc" + "_"+ str(index)
    with open(os.path.join(output_dir, out_file_name + ".json"),
              'w') as out_file:
        json.dump(funcs, out_file)
