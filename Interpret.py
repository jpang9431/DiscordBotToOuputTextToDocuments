import json
import os
import re
import threading

secertFile = open("config.json")
fileData = json.load(secertFile)
fullTextOutputFilePath = fileData["fullTextOutputFilePath"]
sepicalTextOutputFilePath = fileData["sepicalTextOutputFilePath"]

wordCountFilePath = fileData["wordCountFile"]
specialCountFilePath = fileData["specialCountFile"]
charCountFilePath = fileData["characterCountFile"]

def addWordsToDictionary(dict, everyoneDict, words):
    for word in words:
        if word:
            if (word in dict):
                dict[word] = dict[word]+1
            else:
                dict[word] = 1
            if (word in everyoneDict):
                everyoneDict[word] = everyoneDict[word]+1
            else:
                everyoneDict[word] = 1

def writeToFileFromDict(filePath, dictionary):
    with open (filePath, "w", encoding="utf-8") as f:
        f.write("{")
        count = 0
        numDicts = len(dictionary)
        for key in dictionary.keys():
            string = "\n"
            count+=1
            if (count<numDicts):
                string = ","+string
            tempDict = dictionary[key]
            f.write('"'+key+'":')
            f.write(json.dumps(sorted(tempDict.items(), key=lambda item: item[1], reverse=True), ensure_ascii=False)+string)
        f.write("}")
        f.close()

def interpretMessage():
    userWordsDictionary = dict()
    userWordsDictionary["Everyone"] = dict()
    userSpeical = dict()
    userSpeical["Everyone"] = dict()
    userChar = dict()
    userChar["Everyone"] = dict()
    speical = "("
    with open(sepicalTextOutputFilePath, "r", encoding="utf8") as f:
        lines = f.readlines()
        for line in lines:
            list = line.split(",")
            speical+=list[1]
            speical+="|"
        speical = speical[:-1]
        speical += ")+"
        f.close()
    speicalRegEx = re.compile(speical)
    wordRegEx = re.compile(r'\w+|[^\s\w]')
    file = open(fullTextOutputFilePath, "r", encoding="utf8")
    lines = file.readlines()
    for line in lines:
        list = line.split(",",1)
        user = list[0]
        speicalWords = re.findall(speicalRegEx, list[1])
        words = re.findall(wordRegEx, list[1])
        chars = re.findall(r".",list[1])
        if not user in userSpeical:
            userSpeical[user] = dict()
            userChar[user] = dict()
            userWordsDictionary[user] = dict()
        userSpeicalDict = userSpeical[user]
        userWordsDict = userWordsDictionary[user]
        userCharDict= userChar[user]
        speicalThread = threading.Thread(target=addWordsToDictionary, args=(userSpeicalDict, userSpeical["Everyone"], speicalWords))
        wordThread = threading.Thread(target=addWordsToDictionary, args=(userWordsDict, userWordsDictionary["Everyone"], words))
        charThread = threading.Thread(target=addWordsToDictionary, args=(userCharDict, userChar["Everyone"], chars))
        speicalThread.start()
        wordThread.start()
        charThread.start()
        speicalThread.join()
        wordThread.join()
        charThread.join()
    addWords = threading.Thread(target=writeToFileFromDict, args=(wordCountFilePath, userWordsDictionary))
    addSpecials = threading.Thread(target=writeToFileFromDict, args=(specialCountFilePath, userSpeical))
    addChars = threading.Thread(target=writeToFileFromDict, args=(charCountFilePath, userChar))
    addWords.start()
    addSpecials.start()
    addChars.start()
    addWords.join()
    addSpecials.join()
    addChars.join()
    print("Done")
    file.close()

interpretMessage()