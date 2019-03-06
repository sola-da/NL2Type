# NL2Type 🔵
NL2Type: Inferring JavaScript Function Types from Natural Language Information

[ICSE'19 paper](http://software-lab.org/publications/icse2019_NL2Type.pdf)

## Using Docker for replication
### Install docker
Install _docker_ for your environment. We have tested on docker version 18.09.1, build 4c52b90 on Ubuntu 18.04. One may also follow the official install instructions from here:
https://docs.docker.com/install

### Download data
Download some required data from [this link](https://drive.google.com/file/d/1JUjvliIV76_LtqoZvcIVAOfZUBeGgVFk/view?usp=sharing), unzip and place in the _home_ directory. We refer this unzipped folder as the **data** folder throughout this documentation. You may also put the **data** directory anywhere but while running the docker containers, you need to provide the
absolute path of this directory. The following instructions are written with the assumption that
the unzipped _data_ folder is placed in the home directory. Please adapt the absolute path of the _data_ folder according to your environment and USER_NAME.

The template command for running the containers is
```shell
docker pull jibesh/nl2type:TAG
docker run -v PATH_TO_DATA_DIR:/data jibesh/nl2type:TAG
```

PS: You might need to prepend _sudo_ to each of the following commands

### Download the containers

1. To replicate the results from Table 1 of our paper, run the following commands:
```shell
# Pull the container
docker pull jibesh/nl2type:table1
# Execute the script
docker run -v /home/USER_NAME/data:/data jibesh/nl2type:table1
```
Results are printed on the terminal which corresponds to the first row of Table 1 (Approach: NL2Type) of
our paper.
The final output of this command is placed in _data/paper/results/results.csv_

2. To replicate the results for the model trained only on names and not on the comments is
```shell
docker pull jibesh/nl2type:table1_no_comments
docker run -v /home/USER_NAME/data:/data jibesh/nl2type:table1_no_comments
```
Results are printed on the terminal which corresponds to the second row of Table 1 (Approach: NL2Type w/o comments) of our paper.
The final output of this command is placed in *data/paper/results/predictions_paper_no_comments.csv*

3. To use the model to make predictions using the same _test_ data as used in the paper, run the following commands. The test data is placed in *data/paper/raw_csv/test.csv*
```shell
docker pull jibesh/nl2type:from_vecs
docker run -v /home/USER_NAME/data:/data jibesh/nl2type:from_vecs
```
The final output of this command is placed in *data/paper/results\_new\_enriched.csv*. This script first vectorizes the data in this test file and uses the same model as used in the paper to make predictions. This corresponds to steps 3, 4 and 5 in Figure 2 in the paper.

4. Finally, if you want to use our tool using your own set of JavaScript files, you may run the following
commands. Please ensure that the used JavaScript files have some JSDoc annotations since these will be used for extracting the natural language information used for training and testing the model. Additionally, there need be enough JavaScript files to learn from and providing only a few examples might not give the desired output. The set of JavaScript files must be placed in the _data_ folder to the path →
_/data/demo/files_. To use the JavaScript files used by us, you may download some of them from this [link](https://drive.google.com/open?id=1tk-h3O-nTQ3X-cPZ5D7aaaLTUtLgVvwt). Next run the following commands.
```shell
docker pull jibesh/nl2type:demo
docker run -v /home/USER_NAME/data:/data jibesh/nl2type:demo
```
The predictions for the given files will be *data/demo/results/results.csv*


If you **do not** want to use docker please use the following setup setup and instructions
to run our tool.

## Requirements and assumptions
- python 2.7
- pip2 (Tested using version 9.0.1 for python 2)
- Tested on Ubuntu 18.04.1 LTS

## Download data

- Download some results and required data from [this link](https://drive.google.com/file/d/1JUjvliIV76_LtqoZvcIVAOfZUBeGgVFk/view?usp=sharing), place it in _current directory_ and unzip it.

- To download the files used for training and testing the model used in the paper, [use this link](https://drive.google.com/open?id=1tk-h3O-nTQ3X-cPZ5D7aaaLTUtLgVvwt). The files used for training the model are in "training_files" and the files used in testing are in "testing_files"

## Setup steps

- Install the dependencies using the following command
```shell
pip2 install --upgrade -r requirements.txt
```

- Install Node.js and also download a required Node.js package using the following command
```shell
sudo apt-get install -y nodejs
npm install -g jsdoc
```

## Results and replication

- The model used in the paper is in models/model.h5

- The main results file from the paper is data/paper/results/results.csv. The following commands calculate the results in Table 1 in the paper from this results file:
```shell
python2 scripts/runner.py --config scripts/configs/stats_paper.json
```
The results for the model trained only on names and not on comments is data/paper/results/predictions\_paper\_no\_comments.csv. The following commands calculate the results for no comments in Table 1 in the paper from this file:
```shell
python2 scripts/runner.py --config scripts/configs/stats_paper_no_comments.json
```
In the results file, the column "original" contains the actual type of the datapoint, the column "top\_5\_prediction" refer to the top 5 most likely predictions as explained in the paper, separated by the token "%".
The column "datapoint_type" indicated whether the point is a function or parameter, with the value 0 for a function and 1 for a parameter.

- To use the model to make predictions using the same test data as used in the paper, run the following command:
```shell
python2 scripts/runner.py --config scripts/configs/from_vecs.json
```
This makes predictions for the points present in the file data/paper/raw\_csv/test.csv and
the generated results file will be data/paper/results\_new\_enriched.csv

- The results from the inconsistency analysis are in data/paper/results/inconsistency_analysis_paper.csv

## Demo

- To make predictions on some Javascript files of your own choosing, using the model used in the paper, place some Javascript files in data/demo/files and then run the following command:
```shell
python2 scripts/runner.py --config scripts/configs/demo.json
```
Please ensure that the used JavaScript files have some JSDoc annotations since these will be used for extracting the natural language information used for training and testing the model.
The predictions for the files will be data/demo/results/results.csv
