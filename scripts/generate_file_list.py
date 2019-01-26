import os
from random import shuffle


def invoke(config):
    files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(config['input_dir']) for f in filenames if f.endswith(config['extension'])]
    shuffle(files)
    # files_training = files[:int(len(files) * .8)]
    # files_testing = files[int(len(files) * .8):]
    #

    with open(os.path.join(config['output_dir'], "files.txt"), 'w') as f:
        for f_t in files:
	    try:
            	f.write(f_t + "\n")
	    except:
		continue

    # with open(os.path.join(config['output_dir'], "testing.txt"), 'w') as f:
    #     for f_t in files_testing:
    #         f.write(f_t + "\n")

