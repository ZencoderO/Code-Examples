import pickle
from tabulate import tabulate
from operator import itemgetter

def dumpit (name, graph):
    f = file (name, "w")
    pickle.dump(graph,f)
    f.close ()

def returnInd(f):
    line = f.readline()
    headers = line.split(",")
    ind = dict()
    for i in range(0, len(headers)):
        ind[headers[i]] = i
    return ind

def return_graph_user(f,ind, fileName):
    dictGraphUser = {}
    while True:
        line = f.readline()
        if line == "":
            break
        values = line.split(",")
        name = values[ind["screen_name"]]
        if int(values[ind["R"]]) == 1:
            if not dictGraphUser.__contains__("R"):
                dictGraphUser["R"] = []
            dictGraphUser["R"].append(name)
        if int(values[ind["RXM"]]) == 1:
            if not dictGraphUser.__contains__("RXM"):
                dictGraphUser["RXM"] = []
            dictGraphUser.get("RXM").append(name)
        if int(values[ind["M"]]) == 1:
            if not dictGraphUser.__contains__("M"):
                dictGraphUser["M"] = []
            dictGraphUser.get("M").append(name)
        if int(values[ind["XBIN"]]) == 1:
            if not dictGraphUser.__contains__("XBIN"):
                dictGraphUser["XBIN"] = []
            dictGraphUser.get("XBIN").append(name)
        if int(values[ind["BIN"]]) == 1:
            if not dictGraphUser.__contains__("BIN"):
                dictGraphUser["BIN"] = []
            dictGraphUser.get("BIN").append(name)
        if int(values[ind["TH"]]) == 1:
            if not dictGraphUser.__contains__("TH"):
                dictGraphUser["TH"] = []
            dictGraphUser.get("TH").append(name)
        if int(values[ind["CH"]]) == 1:
            if not dictGraphUser.__contains__("CH"):
                dictGraphUser["CH"] = []
            dictGraphUser.get("CH").append(name)

    return dictGraphUser

def returnLength(list1, list2):
    return len(list(list1.intersection(list2)))

def printstatInBothFile(dictF, dictG):
    CommonInBoth = []
    LengthInMasterFile = []
    LengthInMaster3File = []
    InMasterFile = []
    InMaster3File = []

    R = []
    RXM = []
    M = []
    XBIN = []
    BIN = []
    TH = []
    CH = []

    R.extend(("R",returnLength(set(dictF["R"]), set(dictG["R"])),
              len(set(dictF["R"]) - set(dictG["R"])),
              len(set(dictG["R"]) - set(dictF["R"])),
              str(set(dictF["R"]) - set(dictG["R"])),
              str(set(dictG["R"]) - set(dictF["R"]))))

    RXM.extend(("RXM", returnLength(set(dictF["RXM"]), set(dictG["RXM"])),
              len(set(dictF["RXM"]) - set(dictG["RXM"])),
              len(set(dictG["RXM"]) - set(dictF["RXM"])),
              str(set(dictF["RXM"]) - set(dictG["RXM"])),
              str(set(dictG["RXM"]) - set(dictF["RXM"]))))

    XBIN.extend(("XBIN", returnLength(set(dictF["XBIN"]), set(dictG["XBIN"])),
              len(set(dictF["XBIN"]) - set(dictG["XBIN"])),
              len(set(dictG["XBIN"]) - set(dictF["XBIN"])),
              str(set(dictF["XBIN"]) - set(dictG["XBIN"])),
              str(set(dictG["XBIN"]) - set(dictF["XBIN"]))))

    M.extend(("M", returnLength(set(dictF["M"]), set(dictG["M"])),
              len(set(dictF["M"]) - set(dictG["M"])),
              len(set(dictG["M"]) - set(dictF["M"])),
              str(set(dictF["M"]) - set(dictG["M"])),
              str(set(dictG["M"]) - set(dictF["M"]))))

    BIN.extend(("BIN", returnLength(set(dictF["BIN"]), set(dictG["BIN"])),
                 len(set(dictF["BIN"]) - set(dictG["BIN"])),
                 len(set(dictG["BIN"]) - set(dictF["BIN"])),
                 str(set(dictF["BIN"]) - set(dictG["BIN"])),
                 str(set(dictG["BIN"]) - set(dictF["BIN"]))))

    TH.extend(("TH", returnLength(set(dictF["TH"]), set(dictG["TH"])),
              len(set(dictF["TH"]) - set(dictG["TH"])),
              len(set(dictG["TH"]) - set(dictF["TH"])),
              str(set(dictF["TH"]) - set(dictG["TH"])),
              str(set(dictG["TH"]) - set(dictF["TH"]))))

    CH.extend(("CH", returnLength(set(dictF["CH"]), set(dictG["CH"])),
              len(set(dictF["CH"]) - set(dictG["CH"])),
              len(set(dictG["CH"]) - set(dictF["CH"])),
              str(set(dictF["CH"]) - set(dictG["CH"])),
              str(set(dictG["CH"]) - set(dictF["CH"]))))


    print tabulate([R,RXM,M,XBIN,BIN,TH,CH],
                   headers=['Subgraph','Common User','In Master File', 'In Master 3 File', 'User In Master File', 'User In Master 3 File'  ])


def printstatInBothFile_Black(dictF, dictG):
    CommonInBoth = []
    LengthInMasterFile = []
    LengthInMaster3File = []
    InMasterFile = []
    InMaster3File = []

    R = []
    RXM = []
    M = []
    XBIN = []
    BIN = []
    TH = []
    CH = []

    R.extend(("R",returnLength(set(dictF["R"]), set(dictG["R"])),
              len(set(dictF["R"]) - set(dictG["R"])),
              len(set(dictG["R"]) - set(dictF["R"]))))

    RXM.extend(("RXM", returnLength(set(dictF["RXM"]), set(dictG["RXM"])),
              len(set(dictF["RXM"]) - set(dictG["RXM"])),
              len(set(dictG["RXM"]) - set(dictF["RXM"]))))

    XBIN.extend(("XBIN", returnLength(set(dictF["XBIN"]), set(dictG["XBIN"])),
              len(set(dictF["XBIN"]) - set(dictG["XBIN"])),
              len(set(dictG["XBIN"]) - set(dictF["XBIN"]))))

    M.extend(("M", returnLength(set(dictF["M"]), set(dictG["M"])),
              len(set(dictF["M"]) - set(dictG["M"])),
              len(set(dictG["M"]) - set(dictF["M"]))))

    BIN.extend(("BIN", returnLength(set(dictF["BIN"]), set(dictG["BIN"])),
                 len(set(dictF["BIN"]) - set(dictG["BIN"])),
                 len(set(dictG["BIN"]) - set(dictF["BIN"]))))

    TH.extend(("TH", returnLength(set(dictF["TH"]), set(dictG["TH"])),
              len(set(dictF["TH"]) - set(dictG["TH"])),
              len(set(dictG["TH"]) - set(dictF["TH"]))))

    CH.extend(("CH", returnLength(set(dictF["CH"]), set(dictG["CH"])),
              len(set(dictF["CH"]) - set(dictG["CH"])),
              len(set(dictG["CH"]) - set(dictF["CH"]))))


    print tabulate([R,RXM,M,XBIN,BIN,TH,CH],
                   headers=['Subgraph','In Both','Thank You Stat', 'Thank You plus Black Twitter'])


def userTweets(user):
    f = open("at_multidigraph.pkl")
    J = pickle.load(f)
    f.close()
    listOfTweet = []
    count = 0
    for i, j, data in J.edges(data=True):
        temp = []
        if j in user:
            temp.extend((i,j,data["tokens"]))
            listOfTweet.append(temp)
            count += 1
    print tabulate(sorted(listOfTweet, key=itemgetter(1)),headers=["From User", "To User", "Tweet"])

def main():
    f = file("masterfile.csv")
    g = file("master_3_thanking.csv")
    indF = returnInd(f)
    indG = returnInd(g)
    dictG = return_graph_user(g,indG, "master_3")
    dictF = return_graph_user(f,indF, "master")

    h = file("master_3_BTTerm.csv")
    indM = returnInd(h)
    dictM = return_graph_user(h,indM, "Master Modified")

    print "*********************** Black Term plus Thanking VS Thanking ******************************"
    printstatInBothFile_Black(dictG,dictM)
    print "*********************** Thanking_UR Code VS Thanking_Our Code ******************************"
    printstatInBothFile(dictF, dictG)

    userSet = set()
    for key in dictF:
        for user in set(dictF[key]) - set(dictG[key]):
            userSet.add(user)
        for user in set(dictG[key]) - set(dictF[key]):
            userSet.add(user)
    print "*********************** User Tweet ******************************"
    userTweets(userSet)



if __name__ == '__main__':
    main()