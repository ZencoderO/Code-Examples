import pickle
import pandas

top25Propigated = sorted([150,
222,
242,
228,
246,
234,


                          ])
top25PropigatedNames = sorted([2025,
3202,
3407,
3260,
3460,
3352,


                               ])


class langaugeVector:
    __slots__ = "vocabulary", "vectors"

    def __init__(self, wordCount, corpus, comunityWords):
        self.vocabulary = []
        for x in wordCount.keys():
            self.vocabulary.append(x)
        self.vectors = []
        count = 0
        for x in corpus:
            self.vectors.append(self.selfTFIDF(wordCount, x, comunityWords[count]))
            count += 1

    def selfTFIDF(self, wordCount, line, comunityWords):
        totalValues = {}
        for x in self.vocabulary:
            totalValues[x] = 0
        for x in comunityWords.wordsDict.keys():
            totalValues[x] = comunityWords.wordsDict[x]
        totalDocWords = len(line.split(" "))
        finalResults = []
        for x in totalValues.keys():
            finalResults.append((totalValues[x] / totalDocWords) * wordCount[x])
        return finalResults


class comunityWords:
    __slots__ = "wordsDict", "sortedDict"

    def __init__(self, comunityCorpus):
        self.wordsDict = comunityCorpus
        self.sortedDict = sorted(comunityCorpus.items(), key=lambda x: x[1], reverse=True)


def printWordCounts(obj, coumunities, setToPrint=None):
    """

    :param obj:
    :param coumunities:
    :param setToPrint:
    :return:
    """
    count = 0
    if setToPrint == None:
        setToPrint = coumunities
    for x in coumunities:
        if x in setToPrint:
            print(x)
    for x in obj:
        limit = 30
        if coumunities[count] in setToPrint:
            print("words for " + str(coumunities[count]) + " comunities")
            for y in x.sortedDict:
                print(str(y) + ' ')
                limit -= 1
                if limit == 0:
                    break
        count += 1


def returnFeatureSet(vectors, setToPrint=None, printedNames=None):
    """

    :param vectors:
    :param FeatureSet:
    :param setToPrint:
    :return:
    """
    finalSet = []
    features = vectors.vocabulary
    debug = vectors.vectors
    comunityCount = 0
    for x in vectors.vectors:
        currentSet = {}
        if setToPrint == None or comunityCount in setToPrint:
            count = 0
            for y in features:
                currentSet[y] = x[count]
                count += 1
            finalSet.append(sorted(currentSet.items(), key=lambda x: x[1], reverse=True))
        comunityCount+=1
        """
            for y in x:
                if features[count][:5]!='httpt' and features[count][:5]!='https':
                    comunityValues.append((y,features[count]))
                count+=1
            comunityValues.sort(key=lambda comunityValues: comunityValues[0],reverse=True)
            finalSet.append(comunityValues)
        comunityCount+=1
        """
    count = 0
    WordDict = {'Comunity Number': [], 'topwords': []}
    for line in finalSet:
        output = ''

        wordsFound = 0
        sentinel = 5
        try:
            while wordsFound < (sentinel):
                try:
                    numberPrune = int(line[wordsFound][0])
                    sentinel += 1
                except (TypeError, ValueError):
                    if "user" in str(line[wordsFound][0]):
                        sentinel += 1
                    else:
                        output += str(line[wordsFound][0]) + ","
                wordsFound += 1
            WordDict['topwords'].append(output)
            if output != '':
                if setToPrint != None:
                    WordDict['Comunity Number'].append(str(printedNames[count]))
                else:
                    WordDict['Comunity Number'].append(str(count))

        except IndexError:
            continue

        count += 1
    df = pandas.DataFrame(WordDict)
    print(df.to_latex(index=False))


debug = pickle.load(open("kCoreFeatures.pkl", 'rb'))
debug2 = pickle.load(open("kCoreVectors.pkl", 'rb'))
returnFeatureSet(debug2)
debug = pickle.load(open("Propigated ComunityFeatures.pkl", 'rb'))
debug2 = pickle.load(open("Propigated ComunityVectors.pkl", 'rb'))
returnFeatureSet(debug2, top25Propigated,top25PropigatedNames)


