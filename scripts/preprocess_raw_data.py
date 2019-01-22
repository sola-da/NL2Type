from __future__ import unicode_literals

import json
import os
import re

from nltk import pos_tag, WordNetLemmatizer
from nltk.corpus import wordnet, stopwords

import constants


def normalize_types(data):
    counter = 0
    for function in data:
        counter += 1

        if not 'type' in function['returnParam']:
            function['returnParam']['type'] = '__unknown'

        function['returnParam']['type'] = function['returnParam']['type'].lower()

        for key,value in constants.type_strings_mappings.iteritems():
            function['returnParam']['type'] = function['returnParam']['type'].replace(key,value)

        for param in function['params']:
            if not 'type' in param:
                param['type'] = '__unknown'
            # elif not param['type'].lower() in [x.lower() for x in constants.JSbuiltInObj] and "__UNKNOWN" not in param['type']:
            #     param['type'] = 'object'

            param['type'] = param['type'].lower()

            for key, value in constants.type_strings_mappings.iteritems():
                param['type'] = param['type'].replace(key, value)


def camel_case_tokenize(word):
    matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', word)
    return [m.group(0) for m in matches]


def remove_punctuation_and_linebreaks(sentence):
    if type(sentence) is not str and type(sentence) is not unicode: return sentence
    sentence = re.sub('[^A-Za-z0-9. ?]+', ' ', sentence).replace("?", ".") #we only care about sentences, not about questions.

    sentence = sentence.replace('\n', '')
    sentence = sentence.replace('\r', '')

    #we want to get replace full stops not followed by a space with a space. For example object.property --> object property
    return re.sub('\.(?!\ )', ' ', sentence)


def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return ''


def replace_digits_with_space(sentence):
    return re.sub('[0-9]+', ' ', sentence)


def lemmatize(sentence):
    if (type(sentence) is not str and type(sentence) != unicode) or len(sentence) == 0: return sentence
    words = sentence.split(" ")
    words = [word for word in words if word != '']
    if len(words) == 0: return ""
    word_positions = pos_tag(words)
    lemmatized = []
    for p in word_positions:
        word_pos = get_wordnet_pos(p[1])
        lemmatizer = WordNetLemmatizer()
        try:
            if word_pos != '' and len(word_pos) > 0:
                lemmatized.append(lemmatizer.lemmatize(p[0], pos=word_pos))
            else:
                lemmatized.append(lemmatizer.lemmatize(p[0]))
        except UnicodeDecodeError:
            print "ERROR", word_pos, p[0]
    return " ".join(lemmatized)


def remove_stop_words(sentence):
    if type(sentence) is not str and type(sentence) is not unicode: return sentence
    return ' '.join([word for word in sentence.split(' ') if word not in stopwords.words('english')])


def tokenize(sentence):
    if type(sentence) is not str and type(sentence) is not unicode: return sentence
    sentence = sentence.replace("_", " ");
    words = sentence.split(" ")
    camelcase_toknized = []
    for word in words:
        camelcase_toknized.extend(camel_case_tokenize(word))
    camelcase_toknized = [unicode.lower(x) for x in camelcase_toknized]
    return " ".join(camelcase_toknized)


def invoke(config):
    input_files_dir = config['input_dir']
    output_dir = config['output_dir']
    raw_data_json = []
    num_functions = 0
    for index, file_path in enumerate(os.listdir(input_files_dir)):
        with open(os.path.join(input_files_dir, file_path)) as json_file:
            raw_data_json.extend(json.load(json_file))

        num_functions += len(raw_data_json)
        print 'normalizing functions: ', num_functions
        normalize_types(raw_data_json)

        #camel case tokenize and then lemmatize the relevant fields
        print "lemmatizing ", len(raw_data_json), " functions ", num_functions
        for function_object in raw_data_json:

            function_object['cleaned_name'] = lemmatize(tokenize
                                                        (replace_digits_with_space
                                                                 (function_object['name'])))
            function_object['comment'] = remove_stop_words(lemmatize
                                                           (tokenize(remove_punctuation_and_linebreaks
                                                                     (replace_digits_with_space
                                                                      (function_object['comment'])))))
            function_object['returnParam']['comment'] = remove_stop_words(lemmatize
                                                                          (tokenize
                                                                           (remove_punctuation_and_linebreaks
                                                                            (replace_digits_with_space
                                                                             (function_object['returnParam']['comment'])))))

            for param in function_object['params']:
                if 'name' not in param:
                    param['name'] = ''
                else:
                    param['cleaned_name'] = lemmatize(tokenize
                                                      (replace_digits_with_space
                                                       (param['name'])))
                if not 'comment' in param:
                    param['comment'] = ''
                else:
                    param['comment'] = remove_stop_words(lemmatize
                                                         (tokenize
                                                          (remove_punctuation_and_linebreaks
                                                           (replace_digits_with_space
                                                            (param['comment'])))))

        with open(os.path.join(output_dir  + "preprocessed_raw_data" + str(index) + ".json"), 'w') as outfile:
            json.dump(raw_data_json, outfile)
        raw_data_json = []

    return raw_data_json


