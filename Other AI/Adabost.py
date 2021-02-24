
import math
import os
import pickle
import copy

"""
changes needed 
map weights given to yes/no in entorpy to be equal to the weights that given datapoint has 
make it so that you can call the same element mulitplie times in sequence and that you only terminate based on reaching 
some conclution point
"""
def findPosNeg(contents, weights, elementtest):
    """

    :param contents: data of leaf we are evaluating
    :param elementtest: element we are creating this leaf based on it's true/false level
    :return: a list of elements that should be in each leaf
    """
    trueyes = 0
    trueno = 0
    falseyes = 0
    falseno = 0
    count = 0
    for x in contents:
        if x[elementtest]:
            if x[len(x) - 1]:
                trueyes += weights[count]
            else:
                trueno += weights[count]
        else:
            if x[len(x) - 1]:
                falseyes += weights[count]
            else:
                falseno += weights[count]
        count+=1
    return [trueyes, trueno, falseyes, falseno]


class AdaLeaf:
    __slots__ = "entropy", "parrentNode", "yes", "no"

    def __init__(self,parrentNode  ):
        self.parrentNode = parrentNode

    def __str__(self):
        if self.yes >= self.no:
            return "Yes"
        else:
            return "No"

class stump:
    __slots__ = "stump","weight"
    def __init__(self,stump):
        self.stump=stump
        self.weight=0

class AdaNode:
    __slots__ = "trueNo", "trueYes", "falseNo", "falseYes", "leftLeaf", "rightLeaf", "elementNumber"

    def __init__(self, elementTested, data, wieghts):
        results=findPosNeg(data, wieghts, elementTested)
        self.trueYes=results[0]
        self.trueNo=results[1]
        self.falseYes=results[2]
        self.falseNo=results[3]
        self.elementNumber = elementTested
        self.makeLeaves()
    def makeLeaves(self):
        """
        :return: a node that has properly alocated leafs each with there own entropys
        """
        self.rightLeaf = AdaLeaf(self)
        self.rightLeaf.yes=self.trueYes
        self.rightLeaf.no=self.trueNo
        self.rightLeaf.entropy=leafEntropyCalc(self.rightLeaf)
        self.leftLeaf = AdaLeaf(self)
        self.leftLeaf.yes=self.falseYes
        self.leftLeaf.no=self.falseNo
        self.leftLeaf.entropy = leafEntropyCalc(self.leftLeaf)
    def __str__(self):
        return "Element Used: " + str(self.elementNumber) + " leftNodeElement: " + str(
            self.leftLeaf) + " rightNodeElement: " + str(self.rightLeaf)


def selectFile(filename):
    """
a standard parady checking system to ensure the user opens the correct file
    :return: file, a file that has been successfully opened
    """

    fileNotOpen = True
    while fileNotOpen:
        if os.path.isfile(filename):
            fileNotOpen = False
        else:
            filename = input("wrong name try agin")
            exit(0)
    file = open(filename, 'r', encoding="utf8")
    return file


def interprateData(input):
    """
    :param input: data in the form of a document
    :return: array of arrays where each element in a exterior arrary is a array of the boolean varaibles of each dataPoint
    """
    data = []
    for x in input:
        data.append([])
        splitlines = x.split(" ")
        for y in splitlines:
            if y=="T":
                data[len(data) - 1].append(True)
            else:
                if y=="F":
                    data[len(data) - 1].append(False)
    return data

def leafEntropyCalc(leaf):
    """
    :param Data: data within the leaf itself
    :return: entropy based on leaf data
    """

    entropyOfLeaf = 0
    if leaf.yes==0 and leaf.no==0:
        return 1
    xprob = leaf.yes / (leaf.yes + leaf.no)
    if xprob!=0 and xprob!=1:
        entropyOfLeaf += -1 * (xprob * math.log(xprob)+(1-xprob)*math.log(1-xprob))
    return entropyOfLeaf

def AdaLearning(data, weights, remainingElements,stumps,stumpsWanted):
    while len(stumps)<stumpsWanted:
        bestStump=adaForestLearning(data, remainingElements, weights,len(stumps))
        currentleaf=stump(bestStump)
        changeWeight(weights,data, currentleaf)
        stumps.append(currentleaf)


def changeWeight(weights, data, leaf):
    place=0
    errorWeight=0
    if leaf.stump.trueYes > leaf.stump.trueNo:
        errorWeight += leaf.stump.trueNo/(leaf.stump.trueYes+leaf.stump.trueNo)
        correctRight=True
    else:
        errorWeight += leaf.stump.trueYes/(leaf.stump.trueYes+leaf.stump.trueNo)
        correctRight=False
    if leaf.stump.falseYes > leaf.stump.falseNo:
        errorWeight += leaf.stump.falseNo/(leaf.stump.falseYes+leaf.stump.falseNo)
        correctLeft=True
    else:
        errorWeight += leaf.stump.falseYes/(leaf.stump.falseYes+leaf.stump.falseNo)
        correctLeft=False
    normalizedSum=0
    leaf.weight=math.log((1-errorWeight)/errorWeight)
    for x in data:
        if x[leaf.stump.elementNumber]:
            if correctRight== x[len(x)-1]:
                weights[place]=weights[place]*(errorWeight/(1-errorWeight))
        else:
            if correctLeft== x[len(x)-1]:
                weights[place] = weights[place] * (errorWeight / (1 - errorWeight))
        normalizedSum+=weights[place]
        place+=1
    place=0
    distrubutiableWeight=(1-normalizedSum)/len(data)
    for x in data:
        weights[place]=weights[place]+distrubutiableWeight
        place+=1



def adaRemainderCalc(leaf,data):
    """

    :param leaf: leaf and it's entorpy and data
    :param branch: the orginal branch the leaf is being created from (based on a certain boolean variable
    :return:
    """
    returnValue = (leaf.yes + leaf.no) * leaf.entropy
    return returnValue


def adaForestLearning(data,elements,wieghts,currentstump):
    """

    :param data:tree branch is a decition leaf with at least it's gini inilalized
    :param treebranch: data is our input
    :param usedElements: an array of unused elements in the set
    :return: the best element to use in making the next set of decition trees
    """
    bestGain = 1
    bestLeaf = 0
    for x in elements:
        possibleNode = AdaNode(x,data, wieghts)
        totalentropy = adaRemainderCalc(possibleNode.rightLeaf, data)+adaRemainderCalc(possibleNode.leftLeaf, data)
        if bestGain>totalentropy:
            bestLeaf=copy.copy(possibleNode)
            bestGain=totalentropy
    return bestLeaf

def main():
    stumps=[]
    input=selectFile("trainingData.txt")
    data=interprateData(input)
    usedlist=[]
    weights=[]
    for x in range(len(data[0])-2):
        usedlist.append(x)
    for x in range(len(data)):
        weights.append(1/len(data))
    AdaLearning(data, weights,usedlist,stumps,16)
    out=open("StumpFiles","wb")
    pickle.dump(stumps ,out)
if __name__ == '__main__':
  main()