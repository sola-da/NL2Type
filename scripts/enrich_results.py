import pandas as pd

def invoke(config):
    print "Enriching results"
    df_results = pd.read_csv(config['input_file_path_results'])
    df_data = pd.read_csv(config['input_file_path_data'])

    df_results['datapoint_type'] = df_data['datapoint_type']
    df_results['filename'] = df_data['filename']

    df_results.to_csv(config['output_file_path'])