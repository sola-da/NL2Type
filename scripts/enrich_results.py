import pandas as pd


def invoke(config):
    print "Enriching results"
    df_results = pd.read_csv(config['results_file'])
    df_data = pd.read_csv(config['data_file'])

    df_results['datapoint_type'] = df_data['datapoint_type']
    df_results['cleaned_name'] = df_data['cleaned_name']
    df_results['cleaned_comment'] = df_data['comment']
    df_results['return_param_comment'] = df_data['return_param_comment']
    df_results['params'] = df_data['params']
    df_results['filename'] = df_data['filename']
    df_results['line_number'] = df_data['line_number']
    df_results['original'] = df_data['type']

    df_results.to_csv(config['output_file'], index=False)