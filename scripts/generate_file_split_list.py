import os
from random import shuffle


def invoke(config):
    files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(config['input_dir']) for f in filenames if f.endswith(config['extension'])]
    print len(files)
    shuffle(files)
    files_training = files[:int(len(files) * .8)]
    files_testing = files[int(len(files) * .8):]

    print len(files_training)
    print len(files_testing)

    # with open(os.path.join(config['output_dir'], "training.txt"), 'w') as f:
    #     for f_t in files_training:
    #         f.write(f_t + "\n")
    #
    # with open(os.path.join(config['output_dir'], "testing.txt"), 'w') as f:
    #     for f_t in files_testing:
    #         f.write(f_t + "\n")
