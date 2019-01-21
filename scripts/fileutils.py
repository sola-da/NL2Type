import os
import pandas as pd


def get_df_from_files(dir):
    files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(dir) for f in filenames]

    df_list = []
    for index, file in enumerate(files):
        print file
        print "Reading csv {}/{}".format(index, len(files))
        df_list.append(pd.read_csv(file, index_col=None))
    return pd.concat(df_list, ignore_index=True)


def get_top_n_types(types_file, n):

    print "n is: ", n
    top_n = []
    with open(types_file) as tf:
        lines = tf.readlines()

    for index, line in enumerate(lines):
        if index == n:
            break
        top_n.append(line.split(",")[0])

    top_n.append("other")
    return top_n