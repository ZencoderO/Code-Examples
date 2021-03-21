import math
from math import sin, cos, pi
import pandas as pd
import numpy as np
import pdb
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from surface_env  import *
from matplotlib import animation

def init_layers(nn_architecture, seed = 99):
    np.random.seed()
    number_of_layers = len(nn_architecture)
    params_values = {}

    for idx, layer in enumerate(nn_architecture):
        layer_idx = idx + 1
        layer_input_size = layer["input_dim"]
        layer_output_size = layer["output_dim"]

        params_values['W' + str(layer_idx)] = np.random.randn(
            layer_output_size, layer_input_size) * 0.5
        params_values['b' + str(layer_idx)] = np.random.randn(
            layer_output_size, 1) * 0.5 + .5


    return params_values

def convert_prob_into_class(Y):
	return np.array([[1.0 if i > .5 else 0.0 for i in Y[0]]])

def sigmoid(Z):
    return 1/(1+np.exp(-Z))

def relu(Z):
    return np.maximum(0,Z)

def sigmoid_backward(dA, Z):
    sig = sigmoid(Z)
    return dA * sig * (1 - sig)

def relu_backward(dA, Z):
    dZ = np.array(dA, copy = True)
    dZ[Z < 0] = 0
    return dZ
#currently taking from towarddatasicnece.com need to possiblity find more
def mseDerivations(Y_hat, Y):
    msedf= 2*(Y -Y_hat)
 #   m=len(Y)
  #  cost=(2/m)*np.sum((Y_hat-Y))
    return msedf

def single_layer_forward_propagation(A_prev, W_curr, b_curr, activation="relu"):
    Z_curr = np.dot(W_curr, A_prev) + b_curr

    if activation is "relu":
        activation_func = relu
    elif activation is "sigmoid":
        activation_func = sigmoid
    else:
        raise Exception('Non-supported activation function')

    return activation_func(Z_curr), Z_curr

def full_forward_propagation(X, params_values, nn_architecture, stride, desity):
    memory = {}
    A_curr = X

    for idx, layer in enumerate(nn_architecture):

        layer_idx = idx + 1
        A_prev = A_curr
        if layer["type"]=="maxPool":
            maxPoolFowards(layer, A_prev)
        activ_function_curr = layer["activation"]
        W_curr = params_values["W" + str(layer_idx)]
        b_curr = params_values["b" + str(layer_idx)]
        A_curr, Z_curr = single_layer_forward_propagation(A_prev, W_curr, b_curr, activ_function_curr)

        memory["A" + str(idx)] = A_prev
        memory["Z" + str(layer_idx)] = Z_curr

    return A_curr, memory

def predict_once(x,y, params_values, nn_architecture):
  A_curr, memory = full_forward_propagation([[x],[y]], params_values, nn_architecture)
  return A_curr[0][0]

def get_cost_value(Y_hat, Y,df):
    m = Y_hat.shape[1]
    cost=df(Y_hat,Y,m)
   # cost = -1 / m * (np.dot(Y, np.log(Y_hat).T) + np.dot(1 - Y, np.log(1 - Y_hat).T))
    return np.squeeze(cost)

def get_accuracy_value(Y_hat, Y):
    Y_hat_ = convert_prob_into_class(Y_hat)
    return (Y_hat_ == Y).all(axis=0).mean()

def single_layer_backward_propagation(dA_curr, W_curr, b_curr, Z_curr, A_prev, activation="relu"):

    m = A_prev.shape[1]

    if activation is "relu":
        backward_activation_func = relu_backward
    elif activation is "sigmoid":
        backward_activation_func = sigmoid_backward
    else:
        raise Exception('Non-supported activation function')

    dZ_curr = backward_activation_func(dA_curr, Z_curr)
    dW_curr = np.dot(dZ_curr, A_prev.T) / m
    db_curr = np.sum(dZ_curr, axis=1, keepdims=True) / m
    dA_prev = np.dot(W_curr.T, dZ_curr)

    return dA_prev, dW_curr, db_curr
def findDerivedCost(expected, actual):
    return - (np.divide(expected, actual) - np.divide(1 - actual, 1 - expected))

def full_backward_propagation(Y_hat, Y, memory, params_values, nn_architecture):
    grads_values = {}
    m = Y.shape[1]
    Y = Y.reshape(Y_hat.shape)
    # This is derivative of the original cost function, which is dA_prev/relu cost (binary cross etropy should be name and mse is what we should use
    binary_cross_etropy =  - (np.divide(Y, Y_hat) - np.divide(1 - Y, 1 - Y_hat))

    for layer_idx_prev, layer in reversed(list(enumerate(nn_architecture))):
        layer_idx_curr = layer_idx_prev + 1
        activ_function_curr = layer["activation"]
        dA_curr = binary_cross_etropy
        if layer["type"]=="maxpool":
            maxPoolBackwards(layer_idx_curr, dA_curr)
        A_prev = memory["A" + str(layer_idx_prev)]
        Z_curr = memory["Z" + str(layer_idx_curr)]
        W_curr = params_values["W" + str(layer_idx_curr)]
        b_curr = params_values["b" + str(layer_idx_curr)]

        dA_prev, dW_curr, db_curr = single_layer_backward_propagation(
            dA_curr, W_curr, b_curr, Z_curr, A_prev, activ_function_curr)

        grads_values["dW" + str(layer_idx_curr)] = dW_curr
        grads_values["db" + str(layer_idx_curr)] = db_curr

    return grads_values
def maxPoolFowards(density, stride):
    X_reshaped = X.reshape(n * d, 1, h, w)

    # The result will be 4x9800
    # Note if we apply im2col to our 5x10x28x28 input, the result won't be as nice: 40x980
    X_col = im2col_indices(X_reshaped, size, size, padding=0, stride=stride)

    # Next, at each possible patch location, i.e. at each column, we're taking the max index
    max_idx = np.argmax(X_col, axis=0)

    # Finally, we get all the max value at each column
    # The result will be 1x9800
    out = X_col[max_idx, range(max_idx.size)]

    # Reshape to the output size: 14x14x5x10
    out = out.reshape(h_out, w_out, n, d)

    # Transpose to get 5x10x14x14 output
    out = out.transpose(2, 3, 0, 1)
def maxPoolBackwards(vector, layer):
    desity=layer["desity"]
    stride= layer["stride"]
    layers=[]
    count=0
    #rough aprox
    for x in vector:
        layers.append([])
        for y in x:
            layers[count].append[y]
        count+=1
    # 5x10x14x14 => 14x14x5x10, then flattened to 1x9800
    # Transpose step is necessary to get the correct arrangement
    dout_flat = dout.transpose(2, 3, 0, 1).ravel()

    # Fill the maximum index of each column with the gradient

    # Essentially putting each of the 9800 grads
    # to one of the 4 row in 9800 locations, one at each column
    dX_col[max_idx, range(max_idx.size)] = dout_flat

    # We now have the stretched matrix of 4x9800, then undo it with col2im operation
    # dX would be 50x1x28x28
    dX = col2im_indices(dX_col, (n * d, 1, h, w), size, size, padding=0, stride=stride)

    # Reshape back to match the input dimension: 5x10x28x28
    dX = dX.reshape(X.shape)


def update(params_values, grads_values, nn_architecture, learning_rate):
    for layer_idx, layer in enumerate(nn_architecture):
	    layer_idx += 1
        #question 1 is either refering to here need to know what is ment by tradional title
	    params_values["W" + str(layer_idx)] -= learning_rate * grads_values["dW" + str(layer_idx)]
	    params_values["b" + str(layer_idx)] -= learning_rate * grads_values["db" + str(layer_idx)]
	return params_values

def defaultCost(Y, Y_hat):
    m = Y_hat.shape[1]
    return -1 / m * (np.dot(Y, np.log(Y_hat).T) + np.dot(1 - Y, np.log(1 - Y_hat).T))

def train(X, Y, nn_architecture, epochs, learning_rate,df=None):
    params_values = init_layers(nn_architecture,2)
    cost_history = []
    accuracy_history = []

    for i in range(epochs):
        Y_hat, cashe = full_forward_propagation(X, params_values, nn_architecture)
        cost = get_cost_value(Y_hat, Y, df)
        cost_history.append(cost)
        accuracy = get_accuracy_value(Y_hat, Y)
        accuracy_history.append(accuracy)

        grads_values = full_backward_propagation(Y_hat, Y, cashe, params_values, nn_architecture)
        params_values = update(params_values, grads_values, nn_architecture, learning_rate)

    return params_values, cost_history, accuracy_history

def train_once(X, Y, nn_architecture, learning_rate, params_values, cost_history, accuracy_history, df):

    Y_hat, cashe = full_forward_propagation(X, params_values, nn_architecture)
    if df==None:
        df=defaultCost(Y,Y_hat)
    cost = get_cost_value(Y_hat, Y,df)
    cost_history.append(cost)
    accuracy = get_accuracy_value(Y_hat, Y)
    accuracy_history.append(accuracy)

    grads_values = full_backward_propagation(Y_hat, Y, cashe, params_values, nn_architecture)
    print (grads_values)
    params_values = update(params_values, grads_values, nn_architecture, learning_rate)
    return params_values, cost_history, accuracy_history, Y_hat

class OneStep(object):
    def __init__(self, X, Y, params_values, cost_history, accuracy_history, nn_architecture, input_dim,output_dim,type):
        self.params_values = params_values
        self.cost_history = cost_history
        self.accuracy_history = accuracy_history
        self.nn_architecture = nn_architecture
        self.Xs = X
        self.Ys = Y

    def __call__(self):
        title="function"
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        self.params_values, self.cost_history, self.accuracy_history, _ = train_once(self.Xs, self.Ys, self.nn_architecture, 1.0, self.params_values, self.cost_history, self.accuracy_history)
        #ax = plot(lambda i,j: predict_once(i,j, self.params_values, self.nn_architecture))
        #ax.clear()
        plt.title(title)
        ax.plot_surface(xcalc(x,y, lambda i,j: i), xcalc(x,y, lambda i,j: j), xcalc(x,y, lambda i,j: predict_once(i,j, self.params_values, self.nn_architecture)))
        ax.scatter(self.Xs[0], self.Xs[1], self.Ys, color="red")
        plt.show()

class AnimateTrainer:

    def init(self, X, Y, nn_architecture, epochs, learning_rate, ax):
        self.params_values = init_layers(nn_architecture, None)
        self.cost_history = []
        self.accuracy_history = []
        self.learning_rate = learning_rate
        self.X = X
        self.Y = Y
        self.counter = epochs
        self.nn_architecture = nn_architecture
        self.ax = ax

    def __call__(self):
        self.counter -= 10
        for i in range(10):
            self.params_values, self.cost_history, self.accuracy_history, Y_hat = \
                train_once(self.X, self.Y, self.nn_architecture, self.learning_rate, self.params_values, self.cost_history, self.accuracy_history)
        return self.X, self.Y, Y_hat, self.counter, self.params_values, self.nn_architecture, self.ax


def frames():
    iterater = 1
    while iterater > 0:
        X, Y, Y_hat, iterator, params_values, nn_architecture, ax= animate_train()
        yield [X, Y, params_values, nn_architecture, ax]


def animate(args):
    #fig.clear()
    ax.clear()
    ax.scatter(args[0][0], args[0][1], args[1][0], color="red")
    return ax.plot_surface(xcalc(x,y, lambda i,j: i), xcalc(x,y, lambda i,j: j), xcalc(x,y, lambda i,j: predict_once(i,j, args[2], args[3])))

def animate_n_train(X, Y, nn_architecture, epochs, learning_rate):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(X[0], X[1], Y[0], color="red")
    animate_train = AnimateTrainer()

    def frames():
        iterater = 1
        while iterater > 0:
            X, Y, Y_hat, iterator, params_values, nn_architecture, ax= animate_train()
            yield [X, Y, params_values, nn_architecture, ax]
        return None

    def animate(args):
        ax.clear()
        ax.scatter(args[0][0], args[0][1], args[1][0], color="red")
        return ax.plot_surface(xcalc(x,y, lambda i,j: i), xcalc(x,y, lambda i,j: j), xcalc(x,y, lambda i,j: predict_once(i,j, args[2], args[3])))

    animate_train.init(X, Y, nn_architecture, epochs, learning_rate, ax)
    anim = animation.FuncAnimation(fig, animate, frames=frames)
    plt.show()

