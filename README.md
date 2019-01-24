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
