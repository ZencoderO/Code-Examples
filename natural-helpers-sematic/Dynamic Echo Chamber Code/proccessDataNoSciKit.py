import pickle
import os
import numpy
#customized set of stop words for this dataset
prunedWords=['','user','ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out',
             'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into',
             'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the',
             'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were',
             'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to',
             'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have',
             'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can',
             'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself',
             'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by',
             'doing', 'it', 'how', 'further', 'was', 'here', 'than','you','\"user','out','user','I','I\'m','it\'s','im','u',]

class langaugeVector:
    __slots__ = "vocabulary", "vectors"
    def __init__(self,wordCount,corpus,comunityWords):
        self.vocabulary=[]
        for x in wordCount.keys():
            self.vocabulary.append(x)
        self.vectors=[]
        count=0
        for x in corpus:
            self.vectors.append(self.selfTFIDF(wordCount,x,comunityWords[count]))
            count+=1

    def selfTFIDF(self,wordCount,line,comunityWords):
        totalValues={}
        for x in self.vocabulary:
            totalValues[x]=0
        for x in comunityWords.wordsDict.keys():
            totalValues[x]=comunityWords.wordsDict[x]
        totalDocWords=len(line.split(" "))
        finalResults=[]
        for x in totalValues.keys():
            finalResults.append((totalValues[x]/totalDocWords)*wordCount[x])
        return finalResults



class comunityValues:
    __slots__ = "graphType", "comunityOne", "comunityTwo", "distance"

    def __init__(self,graphType, comunityOne, comunityTwo, distance):
        self.graphType=graphType
        self.comunityOne=comunityOne
        self.comunityTwo=comunityTwo
        self.distance=distance
    def __lt__(self, other):
        if self.comunityTwo!=other.comunityOne or self.comunityOne!=other.comunityTwo:
            return self.distance<other.distance

    def __gt__(self, other):
        if self.comunityTwo!=other.comunityOne or self.comunityOne!=other.comunityTwo:
            return self.distance>other.distance
    def __str__(self):
        return str(self.graphType)+" "+str(self.comunityOne)+" "+str(self.comunityTwo)+" "+str(self.distance)
class comunityWords:

    __slots__ = "wordsDict","sortedDict"

    def __init__(self,comunityCorpus):
        self.wordsDict=comunityCorpus
        self.sortedDict=sorted(comunityCorpus.items(), key=lambda x: x[1], reverse=True)
    #def insert(self,dict):


def alocateTop(value,array):
    """
    simple function to add elemenents to an array such that the array is in decending order in O(n) time
    :param value: value to add
    :param array: array in question
    :return:
    """
    x=0
    while x< len(array):
        if value.comunityOne==array[x].comunityOne and value.comunityTwo==array[x].comunityTwo:
            break
        if value>array[x]:
            array.pop(len(array)-1)
            array.insert(x,value)
            break
        x+=1
def createVect(file,runs,dictName):
    """
    :param file: incoming file
    :param runs: total number of files used
    :param dictName: name of file discribing the comunity in use
    :return: tfidf vectors for the given comunity
    """

    courpus = []
    subwordCount = []
    comunityNumbers = []
    totalWords={}
    x=0
    while x < runs:
        try:
            if os.path.getsize(file + str(x) + " basic.txt") > 5000:
                with open(file+str(x)+' basic.txt', 'r', encoding='utf-8',errors='ignore') as community:
                    sentance = ''
                    wordDict = {}
                    for y in community:
                        splitY = y.split(" ")
                        for z in splitY:
                            if z not in prunedWords and 'user' not in z and len(z)<14:
                                if z=='0tf':
                                    debug=0
                                if not totalWords.__contains__(z):
                                    totalWords[z]=1
                                else:
                                    totalWords[z]+=1
                                if wordDict.__contains__(z):
                                    wordDict[z] += 1
                                else:
                                    wordDict[z] = 1
                                sentance+=z+" "

                    subwordCount.append(comunityWords(wordDict))
                    comunityNumbers.append(x)
                    courpus.append(sentance)
        except FileNotFoundError:
            x+=1
            continue
        x+=1
    for x in totalWords.keys():
        totalWords[x]=len(subwordCount)/totalWords[x]
    ourVects=langaugeVector(totalWords,courpus,subwordCount)
    print("comunities")
    for x in comunityNumbers:
        print(x)
    print("corpus by comunity")
    with open(dictName+"basic.pkl", 'wb') as pickleFile:
        pickle.dump(subwordCount, pickleFile)
    with open(dictName+"basicComunities.pkl", 'wb') as pickleFile:
        pickle.dump(comunityNumbers, pickleFile)

    return [ourVects,comunityNumbers]
def euclideanDistance(vecOne,vecTwo):
    a=numpy.array(vecOne)
    b=numpy.array(vecTwo)
    return numpy.linalg.norm(a-b)
def pairwiseDistance(vecs,type,thisGraph,comunityNumbers):
    """
    :param vecs: group of tfidf vectors based on a given comunity
    :param type: variable for altering the type of messure we are using, is always euclidean for this code
    :param thisGraph: name for the type of comunities we are evaulating
    :param comunityNumbers: array of which comunities we are evauluating
    :return:
    """
    xCount=0
    yCount=0
    x=0
    topTenPercent=[]
    while x<(int((len(vecs.vectors)/10))+6):
        topTenPercent.append(comunityValues(thisGraph,0,0,0))
        x+=1
    x=0
    closestX=[]
    while x<(int(len(vecs.vectors))):
        closestX.append((0, -1) )
        x+=1
    sumDiffence=[]
    skip=0
    for x in vecs.vectors:
        currentSum=0
        for y in vecs.vectors:
            currentComperson = comunityValues(thisGraph, comunityNumbers[xCount], comunityNumbers[yCount],euclideanDistance(x,y))
         #                                     sklearn.metrics.pairwise_distances(x, y, metric=type)[0])
            if (currentComperson.distance < closestX[xCount][0] or closestX[xCount][1] == -1) and xCount != yCount:
                closestX[xCount] = [currentComperson.distance, yCount]
            currentSum+=currentComperson.distance
            if skip!=0:
                skip-=1
                continue
            else:
                alocateTop(currentComperson,topTenPercent)
            yCount += 1
        xCount+=1
        sumDiffence.append(currentSum)
        skip=xCount
        yCount=0

    print('Pairwise distances')
    for x in topTenPercent:
       print(str(x))
    print('closest comunity')
    for x in closestX:
        print(x)
    print('total Distance per comunity')
    for x in sumDiffence:
        print(x)
name="kCore"
comunityData=createVect(name,7,"kCoreWords")
with open(name+"Features.pkl",'wb') as outFile:
    pickle.dump(comunityData[1],outFile)
with open(name+"Vectors.pkl",'wb') as outFile:
    pickle.dump(comunityData[0],outFile)
pairwiseDistance(comunityData[0],'euclidean','kCore',comunityData[1])

name="Propigated Comunity"
comunityData=createVect(name,3910,"PropigatedComWords")


with open(name+"Features.pkl",'wb') as outFile:
    pickle.dump(comunityData[1],outFile)
with open(name+"Vectors.pkl",'wb') as outFile:
    pickle.dump(comunityData[0],outFile)



pairwiseDistance(comunityData[0],'euclidean',"Propigated Comunity",comunityData[1])





