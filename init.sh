# mkdir data
# mkdir data/paper
# mkdir data/demo
# mkdir data/demo/files
# mkdir data/demo/jsdoc_out
# mkdir data/demo/raw_csv
# mkdir data/demo/vecs



echo "Downloading js dataset"


echo "Downloading paper test/train split"
python scripts/data/download_data.py 1tk-h3O-nTQ3X-cPZ5D7aaaLTUtLgVvwt data/paper/test_train.zip

echo "Downloading paper intermediate data"
python scripts/data/download_data.py 11d0PJQCs-BuQf1bV46TWJfQNmrwpK_eH data/paper/intermediate.zip

# unzip ../intermediate_data.zip -d ../data/paper

# python