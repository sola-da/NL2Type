#!/usr/bin/env python2
import time

import argparse
import json
import importlib


parser = argparse.ArgumentParser(description="Preprocess data")
parser.add_argument("--config", help="Path to a config file")
args = parser.parse_args()

with open(args.config) as config_file:
    configs = json.load(config_file)

for module_config in configs:
    if 'meta' in module_config:
        conf_string = json.dumps(module_config['config'])

        for key in module_config['meta']:
            conf_string = conf_string.replace('"' + str(key) + '"', str(module_config['meta'][key]))
            conf_string = conf_string.replace(str(key), str(module_config['meta'][key]))
        print conf_string
        module_config_c = json.loads(conf_string)
    else:
        module_config_c = module_config['config']

    start_time = time.time()
    print "Running script: {}".format(module_config['module'])
    importlib.import_module(module_config['module']).invoke(module_config_c)
    print "Time taken: {} seconds".format(time.time() - start_time)
