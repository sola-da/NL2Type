from __future__ import division
import pandas as pd


def invoke(config):
    results_df = pd.read_csv(config['input_file_path'])
    calculate_f1_scores(results_df)
    print ""
    calculate_top_f1(results_df, 3)
    print ""
    calculate_top_f1(results_df, 5)
    print ""
    calculate_f1_scores_param_func(results_df)


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


def calculate_top_f1(df, k):
    print "Calculating f1 scores for top {}".format(k)
    correct = 0
    total = 0
    # top_k_corpus = ['string', 'number', 'object', 'boolean', 'function']
    for index, row in df.iterrows():
        if row['prediction_string'] == 'other':
            continue
        top_k = row['top_k'].split("%")[:k]
        # top_k = top_k_corpus[:k]
        if row['original'] in top_k:
            correct += 1
        total += 1


    print "correct: ", correct
    print "total predictions: ", total
    print "total data points: ", df.shape[0]
    precision = correct/total
    recall = correct/df.shape[0]
    f1 = 2 * ((precision * recall) / (precision + recall))
    print "Precision top {}: {}".format(k, correct/total)
    print "Recall top {}: {}".format(k, correct/df.shape[0])
    print "F1 top{}: {}".format(k, f1)


def calculate_f1_scores_param_func(df):
    correct = 0
    predictions = 0
    total = df[df['datapoint_type'] == 0].shape[0]
    print "Total number of functions is: ", total
    for index, row in df.iterrows():
        if df.loc[index, 'datapoint_type'] == 1:
            continue
        if row['prediction_string'] != 'other':
            predictions += 1
            if row['original'] == row['prediction_string']:
                correct += 1

    precision = correct / predictions
    recall = correct / total
    f1 = 2 * ((precision * recall) / (precision + recall))
    print "precision of function: {}, recall, {}, f1: {}".format(precision, recall, f1)

    correct = 0
    predictions = 0
    total = df[df['datapoint_type'] == 1].shape[0]
    print "Total number of params is: ", total
    for index, row in df.iterrows():
        if df.loc[index, 'datapoint_type'] == 0:
            continue
        if row['prediction_string'] != 'other':
            predictions += 1
            if row['original'] == row['prediction_string']:
                correct += 1

    precision = correct / predictions
    recall = correct / total
    f1 = 2 * ((precision * recall) / (precision + recall))
    print "precision of param: {}, recall, {}, f1: {}".format(precision, recall, f1)
