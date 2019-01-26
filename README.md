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

- Download some intermediate data from [this link](https://drive.google.com/file/d/1wb_rS3pmMQ2g-YOxenGDKMSFg4kIUciR/view?usp=sharing), place it in _current directory_ and unzip it.

## Setup steps
The steps in this section can be ignored if you are using the docker container

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

## Replicating the results
- The model used in the paper is in models/model.h5

- The files used for training the model are in data/paper/js\_files/training and the files used for testing are in data/paper/js\_files/testing. 

- The main results file from the paper is data/paper/results/results.csv. The following commands calculate the figures in Table 1 in the paper from this results file:
```shell
cd scripts
python runner.py --config configs/stats_paper.json
```
The results for the model trained only on names and not on comments is data/paper/results/predictions\_paper\_no\_comments.csv. The following commands calculate the figures for no comments in Table 1 in the paper from this file:

```shell
cd scripts
python runner.py --config configs/stats_paper_no_comments.json
```

In the results file, the column "original" contains the actual type of the datapoint, the column "top\_5\_prediction" refer to the top 5 most likely predictions as explained in the paper, separated by the token "%".

- To use the model to make predictions using the same test data as used in the paper, run the following commands:
```shell
cd scripts
python runner.py --config/from_vecs.json
```
This makes predictions for the points present in the file data/paper/raw\_csv/test.csv
The generated results file will be data/results\_new\_enriched.csv. 

## Demo

- To make predictions on some Javascript files of your own choosing, using the model used in the paper, place some Javascript files in data/demo/files and then run the following commands:

```shell
cd scripts
python runner.py --config configs/demo.json
```

Please ensure that the Javascript files have some JSDoc annotations as these are used for extracting the natural language information used for training and testing the model.

The predictions for the files will be data/demo/results/results.csv
