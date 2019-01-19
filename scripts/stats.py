from __future__ import division
import pandas as pd


def invoke(config):
    results_df = pd.read_csv(config['input_file_path'])
    calculate_f1_scores(results_df)


def calculate_f1_scores(df):
    correct = 0
    predictions = 0
    total = df.shape[0]

    for index, row in df.iterrows():
        if row['prediction_string'] != 'other':
            predictions += 1
            if row['original'] == row['prediction_string']:
                correct += 1

    print "prediction: {}, correct: {}, total:{}".format(predictions, correct, total)
    precision = correct / predictions
    recall = correct / total
    f1 = 2 * ((precision * recall) / (precision + recall))
    print "precision: {}, recall, {}, f1: {}".format(precision, recall, f1)