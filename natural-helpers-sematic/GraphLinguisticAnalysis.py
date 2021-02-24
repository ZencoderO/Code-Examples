import pickle
import numpy as np
import argparse
from helper_helper import get_neighbors_in

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--terms", help="input file data")
    args = parser.parse_args()
    return args

def getValues (helpernodes, scores, wwbpScores):
    """
    Get the average and medians for the helper nodes and scores.
    :param helpernodes:
    :param scores:
    :param wwbpScores:
    :return:
    """
    ansDict = {}
    posemoScores = []
    negemoScores = []
    openness = []
    agreeableness =[]
    neuroticism =[]
    conscientiousness =[]
    extra =[]
    for helper in helpernodes:
        posemoScores.append(scores[helper]['POSEMO'])
        negemoScores.append(scores[helper]['NEGEMO'])
        openness.append(wwbpScores[helper]['Openness'])
        agreeableness.append(wwbpScores[helper]['Agreeableness'])
        neuroticism.append(wwbpScores[helper]['Neuroticism'])
        conscientiousness.append(wwbpScores[helper]['Conscientiousness'])
        extra.append(wwbpScores[helper]['Extraversion'])

    posemoavg = np.average(posemoScores)
    negemoavg = np.average(negemoScores)
    opennessAvg = np.average(openness)
    agreeablenessAvg = np.average(agreeableness)
    neuroticismAvg = np.average(neuroticism)
    conscientiousnessAvg = np.average(conscientiousness)
    posemoMedian = np.median(posemoScores)
    negemoMedian = np.median(negemoScores)
    ansDict["POSEMO"] = posemoavg, posemoMedian
    ansDict["NEGEMO"] = negemoavg, negemoMedian
    ansDict["Agreeableness"] =  agreeablenessAvg, posemoMedian
    ansDict["Neuroticism"] =  neuroticismAvg, negemoMedian
    ansDict["Conscientiousness"] =  conscientiousnessAvg, posemoMedian
    ansDict["Openness"] = opennessAvg, negemoMedian
    ansDict["Extraversion"] = opennessAvg, negemoMedian
    return ansDict



def main():
    ansDict ={}
    args = parse_args()
    terms = args.terms

    fneg1 = open('thank_you_graph_%s.pkl' % terms, 'rb')
    ThankHelpers = pickle.load(fneg1)
    ThankHelpers = ThankHelpers.nodes()
    
 
    f = open("at_graph.pkl")
    atGraph_graph = pickle.load(f)
    f.close() 
    f0 = open('thank_you_no_binaries_%s.pkl' % terms, 'rb')
    mainHelpers = pickle.load(f0)
    mainHelpers = mainHelpers.nodes()
    f = open('thank_you_no_onesies_%s.pkl' % terms, 'rb')
    helpers = pickle.load(f)
    helpernodes = helpers.nodes()
    friends_of_helpers_nodes = get_neighbors_in(helpers, atGraph_graph)
    f2 = open('dictionaryOfScores.pkl', 'rb')
    scores = pickle.load(f2)
    f3 = open("dictionaryOfScoresWWBP.pkl", 'rb')
    wwbpSocres = pickle.load(f3)
    atGraph = set(scores)
    atminusThank = atGraph.difference(set(ThankHelpers))
    ansDict["R@-RT"] = getValues(atminusThank, scores, wwbpSocres)
    getValues(atminusThank, scores, wwbpSocres)
    ansDict["RT"] = getValues(ThankHelpers, scores, wwbpSocres)
    getValues(ThankHelpers, scores, wwbpSocres)
    ansDict["H"] = getValues(mainHelpers, scores, wwbpSocres)
    getValues(mainHelpers, scores, wwbpSocres)
    ansDict["CH"] =getValues(helpers, scores, wwbpSocres)

    ansDict["R@"] = getValues(atGraph, scores, wwbpSocres)

    TerminalHelpers = set(mainHelpers).difference(helpers)
    ansDict["H-CH"] = getValues(TerminalHelpers, scores, wwbpSocres)
    ansDict["NCH"] = getValues(friends_of_helpers_nodes, scores, wwbpSocres)
    f = open("LinguisticAnalysis_%s.pkl" % terms, "wb")
    pickle.dump(ansDict, f)

if __name__ == '__main__':
    main()
