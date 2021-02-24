from keras.models import Model
from keras.layers import Input, LSTM, Dense, Embedding
import numpy as np

latent_dim = 50

def returnModel(num_encoder_tokens, num_decoder_tokens,mapOfWordToInt, glovePath):

    embeddings_index = {}
    f = open(glovePath)
    for line in f:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        embeddings_index[word] = coefs
    f.close()

    embedding_matrix = np.zeros((len(mapOfWordToInt) + 1, 50))
    for word, i in mapOfWordToInt.items():
        embedding_vector = embeddings_index.get(word)
        if embedding_vector is not None:
            # words not found in embedding index will be all-zeros.
            embedding_matrix[i] = embedding_vector

    # Define an input sequence and process it.
    encoder_inputs = Input(shape=(None,))
    encoder_embedding_layer = Embedding(num_encoder_tokens, latent_dim, weights=[embedding_matrix], trainable=False)(
        encoder_inputs)
    encoder_lstm_layer, state_h, state_c = LSTM(latent_dim, return_state=True)(encoder_embedding_layer)
    encoder_states = [state_h, state_c]
    # Set up the decoder, using `encoder_states` as initial state.
    decoder_inputs = Input(shape=(None, num_decoder_tokens))
    decoder_lstm_layer = LSTM(latent_dim, return_sequences=True)(decoder_inputs, initial_state=encoder_states)
    decoder_dense = Dense(num_decoder_tokens, activation='softmax')
    decoder_outputs = decoder_dense(decoder_lstm_layer)
    # Define the model that will turn
    # `encoder_input_data` & `decoder_input_data` into `decoder_target_data`
    model = Model([encoder_inputs, decoder_inputs], decoder_outputs)

    # Compile & run training categorical_crossentropy, mean_squared_error
    model.compile(optimizer='Adagrad', loss='categorical_crossentropy', metrics=['acc'])
    # Note that `decoder_target_data` needs to be one-hot encoded,
    # rather than sequences of integers like `decoder_input_data`!

    encoder_model = Model(encoder_inputs, encoder_states)

    decoder_state_input_h = Input(shape=(latent_dim,))
    decoder_state_input_c = Input(shape=(latent_dim,))
    decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]
    decoder_lstm = LSTM(latent_dim, return_sequences=True, return_state=True)

    decoder_outputs, state_h, state_c = decoder_lstm(
        decoder_inputs, initial_state=decoder_states_inputs)
    decoder_states = [state_h, state_c]
    decoder_outputs = decoder_dense(decoder_outputs)

    decoder_model = Model(
        [decoder_inputs] + decoder_states_inputs,
        [decoder_outputs] + decoder_states)

    return model, encoder_model, decoder_model


