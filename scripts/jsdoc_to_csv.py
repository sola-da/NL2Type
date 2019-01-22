import json

import os
import pandas as pd
import preprocess_raw_data as pp


def get_line_number(function):
    if "meta" in function and "lineno" in function["meta"]:
        return function["meta"]["lineno"]
    else:
        return -1


def get_filename(function):
    if "meta" in function and "filename" in function["meta"] and "path" in function["meta"]:
        return os.path.join(function['meta']['path'],function["meta"]["filename"])
    else:
        return ""


def invoke(config):
    num_comment = 0
    num_names = 0
    num_types = 0
    num_datapoint = 0
    num_params = 0
    num_returnParamComment = 0
    num_filenames = 0
    num_line_no = 0
    num_cleaned_comment = 0

    files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(config['input_dir']) for f in filenames]
    print "the input dir is: {}".format(config['input_dir'])
    print "the number of input files is: ", len(files)


    for file_index, input_file in enumerate(files):
        print ("processing file %d/%d" % (file_index + 1, len(files)))
        pass
        with open(input_file) as f:
            functions_list = json.load(f)

        df = pd.DataFrame()

        type = []
        name = []
        datapoint_type = []
        comment = []
        cleaned_comment = []
        returnParam_comment = []
        params = []
        line_numbers = []
        cleaned_names = []
        filename_list = []
        with_types = 0

        for index, function in enumerate(functions_list):
            line_num = get_line_number(function)
            filename = get_filename(function)


            params_temp = []
            if 'params' in function:
                for param in function['params']:
                    params.append("")
                    returnParam_comment.append("")
                    datapoint_type.append(1)
                    line_numbers.append(line_num)
                    filename_list.append(filename)

                    if "type" in param and "names" in param["type"]:
                        type.append("|".join(param['type']['names']).lower())
                        with_types += 1
                    else:
                        type.append("")
                    if "name" in param:
                        name.append(param["name"])

                        cleaned_name = pp.lemmatize\
                            (pp.remove_punctuation_and_linebreaks
                            (pp.lemmatize
                            (pp.tokenize
                            (pp.replace_digits_with_space(param['name'])))))
                        params_temp.append(cleaned_name)
                        cleaned_names.append(cleaned_name)
                    else:
                        name.append("")
                        cleaned_names.append("")

                    if "description" in param:
                        comment.append(param["description"])
                        cleaned_comment.append(
                            pp.remove_stop_words(
                            pp.lemmatize(
                            pp.tokenize(
                            pp.remove_punctuation_and_linebreaks(
                            pp.replace_digits_with_space(param['description']))))))
                    else:
                        cleaned_comment.append("")
                        comment.append("")

            datapoint_type.append(0)
            returnParam_comment_temp = ""
            if "returns" in function:
                return_type_temp = []
                for return_type in function["returns"]:
                    if "type" in return_type and "names" in return_type["type"]:
                        return_type_temp.extend(return_type["type"]["names"])
                    if "description" in return_type:
                        returnParam_comment_temp += pp.remove_stop_words(
                            pp.lemmatize(
                            pp.tokenize(
                            pp.remove_punctuation_and_linebreaks(
                            pp.replace_digits_with_space(return_type['description'])))))
                type.append("|".join(return_type_temp).lower())
                with_types += 1
            else:
                type.append("")

            returnParam_comment.append(returnParam_comment_temp)

            if "description" in function:
                comment.append(function["description"])
                cleaned_comment.append(
                    pp.remove_stop_words(
                        pp.lemmatize(
                            pp.tokenize(
                                pp.remove_punctuation_and_linebreaks(
                                    pp.replace_digits_with_space(function['description']))))))
            else:
                comment.append("")
                cleaned_comment.append("")

            if len(params_temp) > 0:
                params.append(" ".join(params_temp))
            else:
                params.append("")

            if "name" in function:
                name.append(function["name"].replace(",", ""))
                cleaned_name = pp.lemmatize(pp.tokenize(pp.replace_digits_with_space(function['name'])))
                cleaned_names.append(cleaned_name)
            else:
                name.append("")
                cleaned_names.append("")

            line_numbers.append(line_num)
            filename_list.append(filename)

        num_comment += len(comment)
        num_names += len(name)
        num_types += len(type)
        num_datapoint += len(datapoint_type)
        num_params += len(params)
        num_returnParamComment += len(returnParam_comment)
        num_filenames += len(filename_list)
        num_line_no += len(line_numbers)
        num_cleaned_comment += len(cleaned_comment)

        df = pd.DataFrame.from_dict({"comment": cleaned_comment,
                                     "name": name,
                                     "cleaned_name":cleaned_names,
                                     "filename":filename_list,
                                     "line_number":line_numbers,
                                     "params":params,
                                     "type":type,
                                     "datapoint_type":datapoint_type,
                                     "return_param_comment": returnParam_comment})

        df.to_csv(os.path.join(config["output_dir"], "data_cleaned" + str(file_index) + ".csv"), encoding='utf-8')
        print "writing to file: " + os.path.join(config["output_dir"], "data_cleaned" + str(file_index) + ".csv")
    print "Comment length", num_comment
    print "name length ", num_names
    print "type length ", num_types
    print "datapoint length ", num_datapoint
    print "params length", num_params
    print "return param comment", num_returnParamComment
    print "filenames ", num_filenames
    print "line numbers ", num_line_no
    print "cleaned comment ", num_cleaned_comment