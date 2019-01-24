import tensorflow as tf
import numpy as np
from keras.models import load_model
import pandas as pd
import json


def init_tf():
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    sess = tf.Session(config=config)
    return sess


def invoke(config):
    init_tf()

    model = load_model(str(config['model_path']))
    global graph
    graph = tf.get_default_graph()

    X_data = np.load(str(config['x_path']))
    Y_data = np.load(str(config['y_path']))
    global graph
    with graph.as_default():
        Y_pred = model.predict(X_data)
    # np.save(config['predictions_output_file'], Y_pred)

    with open(config['types_map']) as f:
        types_map = json.load(f)
    types_map = reverse_dict(types_map)

    index = 0
    mismatch = []
    predictions = []
    original = []
    predictions_string = []
    top_k = []

    # df = pd.read_csv(config['input_file'])
    df_test = pd.read_csv(config['input_file'])
    for x in X_data:
        original.append(df_test.loc[index]['type'])
        if index % 100 == 0:
            print index
        prediction = np.argmax(Y_pred[index])
        predictions.append(prediction)
        # print "Prediction is: {}".format(prediction)
        top_k.append(get_top_5(types_map, Y_pred[index]))
        #string += df.loc[index, 'name'] + ":"
        try:
            p = types_map[np.argmax(Y_pred[index])]
            # string += p + "\n"
            predictions_string.append(p)
            # print "Prediction string is: {}".format(p)


        except KeyError:
            # print Y_pred[index]
            # string += "other" + "\n"
            predictions_string.append("unknown")

            # print "Prediction string is: {}".format("unknown")
            # mismatch.append(1)
            original.append(types_map[np.argmax(Y_data[index])])
            index += 1
            continue

        # original.append(types_map[np.argmax(Y_data[index])])
        # if np.argmax(Y_pred[index]) != np.argmax(Y_data[index]):
        #     mismatch.append(1)
        # else:
        #     mismatch.append(0)
        index += 1


    df = pd.DataFrame.from_dict(
        {#"prediction": predictions,
         # "mismatch": mismatch,
         "prediction": predictions_string,
         # "original":original,
         "top_5":top_k})


    df.to_csv(str(config['evaluations_output_file']), index=False)

    return df

def reverse_dict(types_map):
    reversed = {}
    for key, val in types_map.iteritems():
        reversed[val] = key
    return reversed

def get_top_5(types_map, array):
    # print array.shape
    sorted_indices = np.argsort(-array)
    # print sorted_indices
    top_k = []
    for i in range(0,5):
        try:
            top_k.append(types_map[sorted_indices[i]])
        except KeyError:
            top_k.append("unknown")
            continue

    return "%".join(top_k)