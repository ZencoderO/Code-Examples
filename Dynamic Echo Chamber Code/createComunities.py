import pickle
import networkx as nx
import nltk
import sys
import re
#from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
testing=open('/home/lukebat/Documents/testing','r').read()
#from sklearn.feature_extraction.text import TfidfVectorizer
words= set(nltk.corpus.words.words())


# Preprocessing
def remove_string_special_characters(s):
    """
    set of functions desgined to remove words not from engish language, specail characters and whitespace
    :param s: orginal string
    :return: cleaned string
    """
    # removes special characters with ' '
    newdata=s
    range=0
    stripped = re.sub('[^a-zA-z\s]', '', s)
    stripped = re.sub('_', '', stripped)

    # Change any white space to one space
    stripped = re.sub('\s+', ' ', stripped)
    " ".join(w for w in nltk.wordpunct_tokenize(s) \
                 if w.lower() in words or not w.isalpha())
    # Remove start and end white spaces
    stripped = stripped.strip()
    if stripped != '':
        return stripped.lower()

def dataCleaning(data,title):
    """
    proccess desgined to take in strings repersenting the sum total of all interactions in a comunity and save them
    as a seperate file
    :param data: current string passed by user
    :param title: current comunity type and count
    :return: a number of files named after there corsponding comunities
    """
    data=remove_string_special_characters(data)
    with open('/media/lukebat/'+str(title)+' basic.txt', 'w') as json_file:
         json_file.write(data)


def outputPropigatedComunity(generator,graph):
    """
    function desgined to generate the sum total of all converstaions in each comunity found by propigated labbleing
    :param generator: iterator containg the comunity created by Propigated labbeling
    :param graph: orginal directed graph
    :return: file containing cleaned tweet data for a given comunity
    """
    comunity=[]
    for x in generator:
        comunity.append(x)
    count=0
    for x in comunity:
        comunityData=''
        for y in x:
            for z in x:
                try:
                    tweets=graph[y][z]
                    for i in tweets.keys():
                        tweet = tweets[i]['attr_dict']['tokens']
                        try:
                            for h in tweet.split('@'):
                                comunityData+=str('user '+h[h.find(' '):])
                        except ValueError:
                            continue
                except KeyError:
                    continue
        if len(comunityData) > 1:
            dataCleaning(comunityData,'Propigated Comunity'+str(count))
            count+=1

def outPutKCoreComunity(communityList,graph):
    """
    function desgined to generate the sum total of all converstaions in each comunity found by kCore Labbeling
    :param communityList: dictionary containg the comunity created by Propigated labbeling
    :param graph: orginal directed graph
    :return: file containing cleaned tweet data for a given comunity
    """
    communitys={}
    count=0
    for x in communityList.keys():
        if communitys.__contains__(communityList[x]):
            communitys[communityList[x]].append(x)
        else:
            communitys[communityList[x]]=[x]
    for x in communitys.keys():
        comunityData = ''
        for y in communitys[x]:
            for z in communitys[x]:
                try:
                    tweets = graph[y][z]
                    for i in tweets.keys():
                        tweet = tweets[i]['attr_dict']['tokens']
                        try:
                            for h in tweet.split('@'):
                                comunityData+=str('user '+h[h.find(' '):])
                        except ValueError:
                            continue
                except KeyError:
                    continue
        if len(comunityData) > 1:
            dataCleaning(comunityData, 'kCore'+str(count))
            count+=1
def outPutModularity(comunityList,graph):
    """
    function desgined to generate the sum total of all converstaions in each comunity found by the use of odularity
    seperation
    :param generator: list containg the comunity created by Propigated labbeling
    :param graph: orginal directed graph
    :return: file containing cleaned tweet data for a given comunity
    """
    count=0
    coumnity=[]
    for x in comunityList:
        comunityData = ''
        for y in x:
            for z in x:
                try:
                    tweets = graph[y][z]
                    tweet = tweets['tokens']
                    for h in tweet.split('@'):
                        try:
                            comunityData+=str('user '+h[h.find(' '):])
                        except ValueError:
                            continue
                except KeyError:
                    continue
            if len(comunityData) > 1:
                dataCleaning(comunityData, 'Modularity Seperated' + str(count))
                count += 1
        coumnity.append(comunityData)
        count+=1
#opens directed graph element for pulling tweet data for each comunity
with open(sys.argv[0], 'rb') as f:
    G=pickle.load(f)

#opens undiredted graph docuemnt needed for creating comunities
with open(sys.argv[1], 'rb') as f:
    G2=pickle.load(f)

kCore=nx.core_number(G2)
outPutKCoreComunity(kCore,G)

communityGenerator=nx.algorithms.community.label_propagation.label_propagation_communities(G2)
outputPropigatedComunity(communityGenerator,G)
