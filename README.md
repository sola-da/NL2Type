# NL2Type 🔵
NL2Type: Inferring JavaScript Function Types from Natural Language Information

## Requirements and assumptions
- python 2.7
- pip2 (Tested using version 9.0.1 for python 2)
- virtualenv
- Tested on Ubuntu 18.04.1 LTS
- We refer _current directory_ as the directory where the current README.md
resides

## Setup steps

- First install the virtual environment
  pip2 install virtualenv

- Now install the dependencies using the following command
```shell
pip2 install --upgrade -r requirements.txt
```

- Download a required Node.js package using the following command
```shell
npm install jsdoc
```

- Download all required data from this link, place it in _current directory_ and unzip it.

## Replicating the results
- The model used in the paper is in data/paper/model.h5

- The files used for training the model are in data/paper/js_files/training and the files used for testing are in data/paper/js_files/testing. 

- The results file from the paper is data/paper/results.csv. The following commands calculate the figures in Table x in the paper from this results file:
```shell
cd scripts
python runner.py --config configs/stats_paper.json
```
In the results file, the column "original" contains the actual type of the datapoint, the column "top_5_prediction" refer to the top 5 most likely predictions as explained in the paper, separated by the token "%".

- To use the model to make predictions using the same test data as used in the paper, run the following commands:
```shell
cd scripts
python runner.py --config/from_vecs.json
```
The generate results file will be data/results_new_enriched.csv. 

- To train a new model on a new training set:

```shell
cd scripts
python runner.py --config/from_scratch.json
```

Please not that this may take several hours to complete.
## Demo

- To make predictions on some Javascript files of your own choosing, using the model used in the paper, place some Javascript files in data/demo/files and then run the following commands:

```shell
cd scripts
python runner.py --config configs/demo.json
```

Please ensure that the Javascript files have some JSDoc annotations as these are used for extracting the natural language information used for training and testing the model.

The predictions for the files will be data/demo/results/results.csv



- You may skip all of the following steps and simply run _XXXXX_TODO_setup.sh_ from the
current directory to have the setting up of the environment completed. In case
errors are encountered while running _setup.sh_ you may follow these steps.
- First install the virtual environment
  pip2 install virtualenv
- Create and activate it
```shell
  virtualenv -p /usr/bin/python2.7 venv
  source venv/bin/activate
```
- Now install the dependencies using the following command
```shell
pip2 install --upgrade -r requirements.txt
```
- Download a required Node.js package using the following command
```shell
npm install jsdoc
```
- Now __download__ some JavaScript files that will be consumed by NL2Type
to the directory _data/demo/files_
```
wget TODO_XXXXXXXX
```
Alternatively you could also put some JavaScript files containing JSDoc comments
in the directory _data/demo/files_ and run NL2Type

## Running
Once the environment has been setup the next step is to run and replicate the
results. To run, first go to the _script_ directory and then issue the command
```shell
python2 runner.py --config demo.json
```
