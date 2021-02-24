import pickle
import numpy as np


def getValues(helpernodes,scores, wwbpScores):
    posemoScores = []
    negemoScores = []
    openness = []
    agreeableness =[]
    neuroticism =[]
    conscientiousness =[]
    extra =[]
    for helper in helpernodes:
        posemoScores.append(scores[helper]['posemo'])
        negemoScores.append(scores[helper]['negemo'])
        openness.append(wwbpScores[helper]['openness'])
        agreeableness.append(wwbpScores[helper]['agreeableness'])
        neuroticism.append(wwbpScores[helper]['neuroticism'])
        conscientiousness.append(wwbpScores[helper]['conscientiousness'])
        extra.append(wwbpScores[helper]['extra'])
    posemoavg = np.average(posemoScores)
    negemoavg = np.average(negemoScores)
    opennessAvg = np.average(openness)
    agreeablenessAvg = np.average(agreeableness)
    neuroticismAvg = np.average(neuroticism)
    conscientiousnessAvg = np.average(conscientiousness)
    posemoMedian = np.median(posemoScores)
    negemoMedian = np.median(negemoScores)
    print("Posemo",posemoavg, posemoMedian)
    print("Neg:", negemoavg, negemoMedian)
    print("agreeableness", agreeablenessAvg, posemoMedian)
    print("neuroticism", neuroticismAvg, negemoMedian)
    print("conscientiousness", conscientiousnessAvg, posemoMedian)
    print("openness:", opennessAvg, negemoMedian)
    print('extra',np.mean(extra),np.median(extra))


def main():
    f0 = open('thank_you_no_binaries.pkl', 'rb')
    mainHelpers = pickle.load(f0)
    f = open('thank_you_no_onesies.pkl','rb')
    helpers = pickle.load(f)
    helpernodes =helpers.nodes()
    f2 = open('dictionaryOfScores.pkl', 'rb')
    scores =  pickle.load(f2)
    f3 = open("dictionaryOfScoresWWBP.pkl",'rb')
    wwbpSocres = pickle.load(f3)

    print ("HelperNodes")
    getValues(helpernodes,scores, wwbpSocres)
    print("Non Helpers")
    nonHelpers = set(scores).difference(set(helpernodes))
    nonHelpers = nonHelpers.difference(set(mainHelpers))
    getValues(nonHelpers,scores, wwbpSocres)
    # f3 = open('helperScores.pkl', 'wb')
    # pickle.dump(helperScores,f3)
    # f3.close()
    f2.close()



if __name__ == '__main__':
    main()