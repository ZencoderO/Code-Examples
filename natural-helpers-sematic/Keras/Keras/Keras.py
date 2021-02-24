# -*- coding: utf-8 -*-
import pandas as pd
from KerasModel import returnModel
import numpy as np
from sklearn.metrics import classification_report
import sys
import pickle
import os
import pdb


def decode_sequence(input_seq, target_characters, rv_target_characters, encoder_model, num_decoder_tokens, decoder_model, max_decoder_seq_length):
    # Encode the input as state vectors.

    states_value = encoder_model.predict(input_seq)

    # Generate empty target sequence of length 1.
    target_seq = np.zeros((1, 1, num_decoder_tokens))
    # Populate the first character of target sequence with the start character.
    target_seq[0, 0, target_characters['\t']] = 1.

    # Sampling loop for a batch of sequences
    # (to simplify, here we assume a batch of size 1).
    stop_condition = False
    decoded_sentence = ''
    while not stop_condition:
        output_tokens, h, c = decoder_model.predict(
            [target_seq] + states_value)
        # Sample a token
        sampled_token_index = np.argmax(output_tokens[0, -1, :])

        sampled_char = rv_target_characters[sampled_token_index]
        decoded_sentence += sampled_char

        # Exit condition: either hit max length
        # or find stop character.
        if (sampled_char == '\n' or
           len(decoded_sentence) > max_decoder_seq_length):
            stop_condition = True

        # Update the target sequence (of length 1).
        target_seq = np.zeros((1, 1, num_decoder_tokens))
        target_seq[0, 0, sampled_token_index] = 1.

        # Update states
        states_value = [h, c]

    return decoded_sentence

def dumpit (name, graph):
    f = file (name, "w")
    pickle.dump(graph,f)
    f.close ()

def encodeToLabelData(df):
    m = []
    m.append(2)
    m.append(df)
    m.append(3)
    return m

def isNotEmpty(s):
    try:
        return bool(s["Tweet"] and s["Tweet"].strip())
    except:
        False

def main ():
    
    reload(sys)
    sys.setdefaultencoding('utf8')

    mapOfIntToWord = dict()
    mapOfWordToInt = dict()
    indexOfMap = 0
    labelIndex = "Rinkesh_Label"
    train = pd.DataFrame.from_csv(os.path.dirname(__file__) + '/../train.csv')
    validate = pd.DataFrame.from_csv(os.path.dirname(__file__) + '/../validate.csv')

    target_characters = dict()
    target_characters['\t'] = 2
    target_characters['\n'] = 3
    target_characters['y'] = 0
    target_characters['n'] = 1
    target_characters['m'] = 1

    rv_target_characters = dict()
    rv_target_characters[0] = 'y'
    rv_target_characters[1] = 'n'
    #rv_target_characters[2] = 'm'
    rv_target_characters[2] = '\t'
    rv_target_characters[3] = '\n'


    train["Tweet_Empty"] = train.apply(isNotEmpty, axis=1)
    train = train[train["Tweet_Empty"] == True]
    train_tweet = train["Tweet"].tolist()

    validate["Tweet_Empty"] = validate.apply(isNotEmpty, axis=1)
    validate = validate[validate["Tweet_Empty"] == True]

    validate[labelIndex] = validate[labelIndex].apply(lambda n : "n" if n == "m" else n)

    train["label"] = train[labelIndex].apply(lambda n : target_characters[n]).tolist()

    train["label"] = train["label"].apply(encodeToLabelData)
    labels = train["label"].tolist()

    for twe in train_tweet:
        twe = twe.split()
        for data in twe:
            if not mapOfWordToInt.__contains__(data):
                # Store the Int to word and vice versa
                mapOfWordToInt[data] = indexOfMap
                mapOfIntToWord[indexOfMap] = data
                indexOfMap += 1

    num_encoder_tokens = indexOfMap + 1
    max_encoder_seq_length = max([len(txt.split()) for txt in train_tweet])
    num_decoder_tokens = 4
    max_decoder_seq_length = 3


    encoder_input_data = np.zeros((len(train), max_encoder_seq_length), dtype='float32')
    decoder_target_data = np.zeros((len(train), max_decoder_seq_length, num_decoder_tokens), dtype='float32')
    decoder_input_data = np.zeros((len(train), max_decoder_seq_length, num_decoder_tokens), dtype='float32')

    for i, (inp, out) in enumerate(zip(train_tweet, labels)):
        inp = inp.split()
        for t, word in enumerate(inp):
            encoder_input_data[i, t + max_encoder_seq_length - len(inp)] = mapOfWordToInt[word]
        for t, char in enumerate(out):
            # decoder_target_data is ahead of decoder_input_data by one timestep
            decoder_input_data[i, t, char] = 1.
            if t > 0:
                # decoder_target_data will be ahead by one timestep
                # and will not include the start character.
                decoder_target_data[i, t - 1, char] = 1.

    model, encoder_model, decoder_model = returnModel(num_encoder_tokens, num_decoder_tokens,mapOfWordToInt,sys.argv[1])

    model.fit([encoder_input_data, decoder_input_data], decoder_target_data,
              batch_size=1,
              epochs=8,verbose=2)


    # Now Preparing test the data
    validate_list_tweet = validate["Tweet"].tolist()

    validate_tweet = np.zeros((len(validate_list_tweet), max_encoder_seq_length), dtype='float32')

    for i, inp in enumerate(validate_list_tweet):
        inp = inp.split()
        for t, word in enumerate(inp):
            if mapOfWordToInt.__contains__(word) and t < max_encoder_seq_length:
                validate_tweet[i, max_encoder_seq_length - len(inp) + t] = mapOfWordToInt[word]

    model_output = []

    for seq_index in range(len(validate_list_tweet)):
        input_seq = validate_tweet[seq_index: seq_index + 1]
        decoded_sentence = decode_sequence([input_seq], target_characters, rv_target_characters, encoder_model,num_decoder_tokens, decoder_model, max_decoder_seq_length)
        decoded_sentence = "".join(decoded_sentence.split("\t"))
        model_output.append(decoded_sentence[0])

    ground_truth = validate[labelIndex].tolist()

    pdb.set_trace()
    print "Precision Recall F1Suport Score"
    print "****************************************************************************************"
    print classification_report(model_output, ground_truth)

if __name__ == "__main__":
    main()

