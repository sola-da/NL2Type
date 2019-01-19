import pandas as pd

def invoke(config):
    print "Enriching results"
    df_results = pd.read_csv(config['input_file_path_results'])
    df_data = pd.read_csv(config['input_file_path_data'])
