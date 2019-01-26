import pandas as pd
import sys
from gensim.models import Word2Vec
import numpy as np
import json
import re
import fileutils as fu
import os

WORD_VEC_LENGTH = 100
to_predict_feature = 'type'


features_list = ['comment', 'params', 'cleaned_name', 'return_param_comment']

def invoke(config):

    global WORD_VEC_LENGTH
    WORD_VEC_LENGTH = config["vector_length"]
    df = pd.read_csv(config['input_file_path'])
    if config['batch']:
        output_vecs_batch(df, config)
    else:
        vecs = df_to_vecs(df, Word2Vec.load(config['word2vec_code']), Word2Vec.load(config['word2vec_language']) , config['features'])
        print '\twriting vecs to file'
        np.save(str(config['data_output_file_path']), vecs)
    if 'type_output_file_path' in config:
        types_vec = type_to_vec(df)
        print '\twriting types to file'
        np.save(str(config['type_output_file_path']), types_vec)
        if 'types_map_path' in config:
            types_map = map_type_to_vec(df, types_vec, fu.get_top_n_types(config['types_file'], config['types_count']))
            with open(config['types_map_path'], 'w') as types_file:
                json.dump(types_map, types_file)


def output_vecs_batch(df, config):
    df_list = np.array_split(df, 4)
    types_vecs = type_to_vec(df)
    types_vecs_list = np.array_split(types_vecs, 4)
    count = 0
    for index, df_t in enumerate(df_list):

        output_file_name = config['out_name'] + "_" + str(index)
        vecs = df_to_vecs(df_t, Word2Vec.load(config['word2vec_code']), Word2Vec.load(config['word2vec_language']),
                          config['features'])
        np.save(os.path.join(config["output_dir"], output_file_name), vecs)

        # types_vecs = type_to_vec(df_t)
        # np.save(os.path.join(config["output_dir_types"], output_file_name), types_vecs)
        np.save(os.path.join(config["output_dir_types"], output_file_name), types_vecs_list[count])

        count += 1

        if count == 0:
            if 'types_map_path' in config:
                types_map = map_type_to_vec(df, types_vecs, fu.get_top_n_types(config['types_file'], config['types_count']))
                with open(config['types_map_path'], 'w') as types_file:
                     json.dump(types_map, types_file)


def type_to_vec(df):
    return pd.get_dummies(df[to_predict_feature]).values


def map_type_to_vec(data, vec, types):
    print '\tMapping types to vec'
    np.set_printoptions(threshold=sys.maxsize)
    types_map = {}
    indices = set()
    for i, t in enumerate(types):
        # if i % 10 == 0:
        #     print i
        try:
            index = data.loc[data['type'].str.match('^' + re.escape(t) + '$')].index[0]
        except IndexError:
            index = - 1

        # array = data.loc[data['type'].str.match('^' + t_escaped + '$')]
        if index == -1:
            index_one_hot = -1
        else:
            index_one_hot = np.where(vec[index] == 1)[0][0]
        if index_one_hot in indices and index_one_hot != -1:
            print "ERRORR ALREADY SEEN"
            print t
            print index_one_hot
        # print index
        indices.add(index_one_hot)

        types_map[t] = index_one_hot
    return types_map


def df_to_vecs(df, w2v_model_code, w2v_model_language, features):
    data = np.zeros((df.shape[0], sum(features.values()) + len(features.values()) - 1, WORD_VEC_LENGTH))
    count = 0
    for index, row in df.iterrows():
        if count % 5000 == 0:
            print "\tProcessed: {} points".format(count)
        data[count] = vectorize_row(row, w2v_model_code, w2v_model_language, np.ones(WORD_VEC_LENGTH), features)
        count += 1
    return data


def vectorize_row(row, w2v_model_code, w2v_model_language, separator, features):
    datapoint = np.zeros((sum(features.values()) + len(features.values()) - 1, WORD_VEC_LENGTH))
    datapoint[0] = vectorize_datapoint_type(row)
    datapoint[1] = separator

    datapoint_index = 2
    # print "Start of row!"
    # for featurename, feature_length in features.iteritems():
    for feature_name in features_list:
        feature_length = features[feature_name]
        # print "Feature name: ", feature_name
        if type(row[feature_name]) is str:
            if feature_name == "cleaned_name" or feature_name == "params":
                vectorized_feature = vectorize_string(row[feature_name], feature_length, w2v_model_code)
            elif feature_name == "comment" or feature_name == "return_param_comment":
                vectorized_feature = vectorize_string(row[feature_name], feature_length, w2v_model_language)

            for word in vectorized_feature:
                datapoint[datapoint_index] = word
                datapoint_index += 1
        elif feature_name != "datapoint_type":
            for i in range(0, feature_length):
                datapoint[datapoint_index] = np.zeros((1, WORD_VEC_LENGTH))
                datapoint_index += 1
        elif feature_name == 'datapoint_type':
            continue

        if datapoint_index >= len(datapoint):
            break

        datapoint[datapoint_index] = separator
        datapoint_index += 1
    return datapoint


def vectorize_datapoint_type(row):
    datapoint_type = np.zeros( (1, WORD_VEC_LENGTH))
    if row['datapoint_type'] == 0:
        datapoint_type[0][0] = 1
    else:
        datapoint_type[0][1] = 1
    return datapoint_type


def vectorize_string(text, feature_length, w2v_model):
    text_vec = np.zeros((feature_length, WORD_VEC_LENGTH))
    if text == 'unknown':
        return text_vec
    count = 0
    for word in text.split():
        if count >= feature_length:
            return text_vec
        try:
            text_vec[count] = w2v_model.wv[word]
        except KeyError:
            pass
        count += 1

    return text_vec


