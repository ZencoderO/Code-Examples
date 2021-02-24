import re
import pandas as pd
from sklearn.model_selection import train_test_split
from PreProcessText import preprocess
import sys
import os.path

'''
Split the Data
'''
def splitTheData(NHDataSetTemp):
    return train_test_split(NHDataSetTemp, test_size=0.2)

'''
Save the csv into train, test and validate after cleaning the text
'''
def saveCSV():
    NHDataSet = pd.DataFrame.from_csv(sys.argv[1], sep=";")
    NHDataSet["Tweet"] = NHDataSet["Tweet"].apply(preprocess)


    train, test = splitTheData(NHDataSet)
    train, validate = splitTheData(train)
    #Saving the Data file
    train.to_csv(os.path.dirname(__file__) + '/../train.csv')
    test.to_csv(os.path.dirname(__file__) + '/../test.csv')
    validate.to_csv(os.path.dirname(__file__) + '/../validate.csv')

saveCSV()


