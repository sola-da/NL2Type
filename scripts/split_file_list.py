import os

def invoke(config):
    with open(config['input_file']) as files:
        files_list = files.read().splitlines()

    files_training = files_list[:int(len(files_list) * .8)]
    files_testing = files_list[int(len(files_list) * .8):]

    with open(os.path.join(config['output_dir'], "training.txt"), 'w') as f:
        for f_t in files_training:
            f.write(f_t + "\n")

    with open(os.path.join(config['output_dir'], "testing.txt"), 'w') as f:
        for f_t in files_testing:
            f.write(f_t + "\n")

