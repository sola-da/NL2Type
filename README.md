# NL2Type 🔵
NL2Type: Inferring JavaScript Function Types from Natural Language Information

## Requirements and assumptions
These are already satisfied if you are using the docker container
- python 2.7
- pip2 (Tested using version 9.0.1 for python 2)
- virtualenv
- Tested on Ubuntu 18.04.1 LTS
- We refer _current directory_ as the directory where the current README.md
resides

## Download data

- Download some results and required data from [this link](https://drive.google.com/file/d/1JUjvliIV76_LtqoZvcIVAOfZUBeGgVFk/view?usp=sharing), place it in _current directory_ and unzip it.

- To download the files used for training and testing the model used in the paper, [use this link](https://drive.google.com/open?id=1tk-h3O-nTQ3X-cPZ5D7aaaLTUtLgVvwt). The files used for training the model are in "training_files" and the files used in testing are in "testing_files"

## Setup steps
The steps in this section can be ignored if you are using the docker container

- Install the dependencies using the following command
```shell
pip2 install --upgrade -r requirements.txt
```

- Install Node.js and also download a required Node.js package using the following command
```shell
sudo apt-get install -y nodejs
npm install jsdoc
```

## Results and replication

- The model used in the paper is in models/model.h5


- The main results file from the paper is data/paper/results/results.csv. The following commands calculate the figures in Table 1 in the paper from this results file:
```shell
python2 scripts/runner.py --config scripts/configs/stats_paper.json
```
The results for the model trained only on names and not on comments is data/paper/results/predictions\_paper\_no\_comments.csv. The following commands calculate the figures for no comments in Table 1 in the paper from this file:

```shell
python2 scripts/runner.py --config scripts/configs/stats_paper_no_comments.json
```

In the results file, the column "original" contains the actual type of the datapoint, the column "top\_5\_prediction" refer to the top 5 most likely predictions as explained in the paper, separated by the token "%".

The column "datapoint_type" indicated whether the point is a function or parameter, with the value 0 for a function and 1 for a parameter.

- To use the model to make predictions using the same test data as used in the paper, run the following commands:
```shell
python2 scripts/runner.py --config scripts/configs/from_vecs.json
```
This makes predictions for the points present in the file data/paper/raw\_csv/test.csv
The generated results file will be data/results\_new\_enriched.csv.

- The results from the inconsistency analysis are in data/paper/results/inconsistency_analysis_paper.csv

## Demo

- To make predictions on some Javascript files of your own choosing, using the model used in the paper, place some Javascript files in data/demo/files and then run the following commands:

```shell
cd scripts
python runner.py --config configs/demo.json
```

Please ensure that the Javascript files have some JSDoc annotations as these are used for extracting the natural language information used for training and testing the model.

The predictions for the files will be data/demo/results/results.csv
