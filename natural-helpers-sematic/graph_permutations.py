import pickle
import liwc.categories
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import user_tweet_collector
import network_analysis
import sys

def getDictDegrees (at_graph):
    dictOfScores = open('dictionaryOfScores.pkl', 'rb')
    dictScores = pickle.load(dictOfScores)
    NumberOfDegrees = at_graph.degree
    degreeUsers ={}
    for user,degrees in NumberOfDegrees:
        if degrees in degreeUsers:
            degreeUsers[degrees]['userList'].append(user)
            degreeUsers[degrees]['scoreList'].append(dictScores[user])
        else:
            degreeUsers[degrees] = {'userList': [user], 'scoreList': [dictScores[user]]}
    return degreeUsers


def segregateGraph (users, scores, avgScore, attribute):
    '''
    Segregates the permuted users above avg and below avg scores
    :param users:
    :param scores:
    :param avgScore:
    :return:
    '''
    segregatedUserSets = {}
    aboveAVG = []
    belowAVG =[]
    for i in range(len(users)):
        user = users[i]
        newScore = scores[i]
        attribute_score = newScore[attribute]
        if attribute_score < avgScore:
            belowAVG.append(user)
        else:
            aboveAVG.append(user)
    segregatedUserSets['aboveAvg'] = aboveAVG
    segregatedUserSets['belowAVG'] = belowAVG
    return segregatedUserSets


def getSegregatedUsersAndScores (attribute):
    '''
    :return:
    '''
    if attribute =='posemo':
        aboveAvg_label = 'aboveAvgPos'
        belowAVG_label = 'belowAVGPOS'
    else:
        aboveAvg_label = 'aboveAvgNeg'
        belowAVG_label = 'belowAVGNeg'

    # get the segregated users
    f = open('segregatedUserSets.pkl', 'rb')
    userSets = pickle.load(f)
    userSets = trimGraph(userSets)
    aboveAvg = list(userSets[aboveAvg_label])
    belowAVG = list(userSets[belowAVG_label])
    aboveAvg.extend(belowAVG)
    scores = []
    dictOfScores = open('dictionaryOfScores.pkl', 'rb')
    dictScores = pickle.load(dictOfScores)
    runningTotal = 0
    for user in aboveAvg:
        scores.append(dictScores[user])
        runningTotal = runningTotal + dictScores[user][attribute]
    avgScore = runningTotal/len(aboveAvg)
    f.close()
    dictOfScores.close()
    return aboveAvg, scores, avgScore


def shuffleForDegrees (degreeDict):
    users=[]
    scores =[]
    for i in degreeDict:
        usersD = degreeDict[i]['userList']
        scoresD = degreeDict[i]['scoreList']
        np.random.shuffle(scores)
        users.extend(usersD)
        scores.extend(scoresD)
    return users,scores


def visualize (dictMedianDiff, realDiff, attribute):
    '''
    :param dictMedianDiff:
    :return:
    '''
    for key in dictMedianDiff:
        values = np.asarray(dictMedianDiff[key])
        counts = np.unique(values,return_counts=True)
        numer= max(counts[1])
        ax = sns.distplot(values, norm_hist=False, kde=False, hist=True, bins=50)
        plt.ylabel("Frequency", fontsize = "large")
        plt.plot([realDiff[key], realDiff[key]],[0,1],'r')
        plt.xlabel("Score", fontsize = "large")
        plt.title(key)
        plt.yticks(fontsize = "large")
        plt.xticks(fontsize="large")
        plt.savefig("Visualizations/" + key + "Permutations" + attribute + ".pdf")
        plt.clf()


def trimGraph (userSets):
    f = open('at_graph.pkl', 'rb')
    at_graph = pickle.load(f)
    f.close()
    nodes = [i[0] for i in at_graph.degree if i[1] > 1]
    nodes = set(nodes)
    for key in userSets:
        users = userSets[key]
        new_users = users.intersection(nodes)
        userSets[key] = new_users
    return userSets


def getActualValues (realDiff, at_graph, attribute):
    """
    Get the observed values from the graph
    :param realDiff: Dictionary to store the values
    :param at_graph: the graph from which the users are generated
    :return:
    """
    users, scores, avgScore = getSegregatedUsersAndScores(attribute)
    segregatedUserSets = segregateGraph(users, scores, avgScore,attribute)
    networkProperties = network_analysis.getPropertyAverages(segregatedUserSets, at_graph)
    aboveAvg = networkProperties['aboveAvg']
    belowAVG = networkProperties['belowAVG']

    for key in aboveAvg:
        value = aboveAvg[key]
        value1 = belowAVG[key]
        diff = value - value1
        realDiff[key] = diff
    print(networkProperties)
    return users, scores, avgScore

def main():
    attribute = sys.argv[1]
    dictMedianDifference = {}
    dictMedianDifference['Triangles'] = []
    dictMedianDifference['Degrees'] = []
    dictMedianDifference['CoreNumbers'] = []
    dictMedianDifference['ClusterCoeffiecients'] = []
    dictMedianDifference['ConnectedComponent'] = []
    dictMedianDifference['BiConnectedComponent'] = []
    dictPvalues = {}
    dictPvalues['Triangles'] = 0
    dictPvalues['Degrees'] = 0
    dictPvalues['CoreNumbers'] = 0
    dictPvalues['ClusterCoeffiecients'] = 0
    dictPvalues['ConnectedComponent'] = 0
    dictPvalues['BiConnectedComponent'] = 0

    f = open('at_graph.pkl', 'rb')
    at_graph = pickle.load(f)
    f.close()
    nodes = [i[0] for i in at_graph.degree if i[1] > 1]
    at_graph = at_graph.subgraph(nodes)
    realDiff = {}

    users, scores, avgPos = getActualValues(realDiff, at_graph, attribute)

    # shuffle the scores
    for i in range(0,10):
        np.random.shuffle(scores)
        segregatedUserSets = segregateGraph(users,scores,avgPos,attribute)
        # get Permutated Graph Properties
        permutedGraphProperties = network_analysis.getPropertyAverages(segregatedUserSets, at_graph)
        aboveAvg = permutedGraphProperties['aboveAvg']
        belowAVG = permutedGraphProperties['belowAVG']
        for key in aboveAvg:
            value = aboveAvg[key]
            value1 = belowAVG[key]
            diff = value - value1
            dictMedianDifference[key].append(diff)
            if diff > realDiff[key]:
                dictPvalues[key] = dictPvalues[key]+1
    visualize(dictMedianDifference,realDiff, attribute)
    medians_file = open('propertyMedianDifferences.pkl', 'wb')
    pickle.dump(dictMedianDifference, medians_file)
    medians_file.close()
    for key in dictPvalues:
        print(key, dictPvalues[key]/10000)

if __name__== '__main__':
    main()