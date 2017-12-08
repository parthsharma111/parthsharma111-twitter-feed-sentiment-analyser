import pickle
import re
import os
from collections import defaultdict
import math

totalDoc = None
totalPositiveFreq = None
totalNegativeFreq = None
totalWords = None
stopWords = None
negationWords = ["not", "didn't", "no", "few", "lacks"]


class Bayes_Classifier_Best_Length:
    positive = defaultdict(int)
    negative = defaultdict(int)
    positive_length = defaultdict(int)
    negative_length = defaultdict(int)

    def __init__(self, trainDirectory="movie_reviews/"):
        global totalDoc
        global totalPositiveFreq
        global totalNegativeFreq
        global totalWords
        global stopWords
        global negationWords

        self.trainDirectory = trainDirectory
        APP_ROOT = os.path.dirname(os.path.abspath(__file__))
        stopWords = self.loadFile(APP_ROOT + "/stop_words.txt")
        try:
            Bayes_Classifier_Best_Length.positive = pickle.load(open(APP_ROOT + "/best_positive.pickle", "rb"))
            Bayes_Classifier_Best_Length.negative = pickle.load(open(APP_ROOT + "/best_negative.pickle", "rb"))
            Bayes_Classifier_Best_Length.positive_length = pickle.load(open(APP_ROOT + "/best_positive_length.pickle", "rb"))
            Bayes_Classifier_Best_Length.negative_length = pickle.load(open(APP_ROOT + "/best_negative_length.pickle", "rb"))
            Bayes_Classifier_Best_Length.results = pickle.load(open(APP_ROOT + "/best_results.pickle", "rb"))
            Bayes_Classifier_Best_Length.totalWords = pickle.load(open(APP_ROOT + "/best_attr.pickle", "rb"))
        except (OSError, IOError) as e:
            print "training"
            Bayes_Classifier_Best_Length.results = {"negative": 0, "positive": 0}
            self.train();

        totalDoc = sum(Bayes_Classifier_Best_Length.results.values())
        totalPositiveFreq = sum(Bayes_Classifier_Best_Length.positive.values())
        totalNegativeFreq = sum(Bayes_Classifier_Best_Length.negative.values())
        totalWords = Bayes_Classifier_Best_Length.totalWords

    def train(self):
        '''Trains the Naive Bayes Sentiment Classifier.'''
        global stopWords

        # 13864 docs
        positiveCount = 0
        negativeCount = 0

        iFileList = []
        Bayes_Classifier_Best_Length.totalWords = 0
        negationFlag = False

        for fFileObj in os.walk(self.trainDirectory):
            iFileList = fFileObj[2]
            break
        print '%d test reviews.' % len(iFileList)

        for filename in iFileList:
            fileText = self.loadFile(self.trainDirectory + filename)
            fileText = fileText.lower();
            rate = filename.split("-")[1]
            state = "positive" if rate == '5' or rate == '4' else "negative"
            if state == "positive":
                if positiveCount > 36664:
                    continue
                positiveCount += 1
            else:
                if negativeCount > 36664:
                    continue
                negativeCount += 1
            tokens = self.tokenize(fileText)
            bestWordCount = len(tokens)
            if state == "positive":
                Bayes_Classifier_Best_Length.positive_length[bestWordCount] += 1
            else:
                Bayes_Classifier_Best_Length.negative_length[bestWordCount] += 1
            for word in tokens:
                if word in [".", ","]:
                    negationFlag = False
                if word in negationWords:
                    negationFlag = True
                if word in stopWords:
                    continue
                if negationFlag:
                    word = "NOT_" + word
                if word not in Bayes_Classifier_Best_Length.positive and word not in Bayes_Classifier_Best_Length.negative:
                    Bayes_Classifier_Best_Length.totalWords += 1
                if state == "positive":
                    Bayes_Classifier_Best_Length.positive[word] += 1
                elif state == "negative":
                    Bayes_Classifier_Best_Length.negative[word] += 1
            # print "%s: %s" % (filename, state)
            Bayes_Classifier_Best_Length.results[state] += 1

        with open('best_positive.pickle', 'wb') as f:
            pickle.dump(Bayes_Classifier_Best_Length.positive, f, pickle.HIGHEST_PROTOCOL)
        with open('best_negative.pickle', 'wb') as f:
            pickle.dump(Bayes_Classifier_Best_Length.negative, f, pickle.HIGHEST_PROTOCOL)
        with open('best_positive_length.pickle', 'wb') as f:
            pickle.dump(Bayes_Classifier_Best_Length.positive_length, f, pickle.HIGHEST_PROTOCOL)
        with open('best_negative_length.pickle', 'wb') as f:
            pickle.dump(Bayes_Classifier_Best_Length.negative_length, f, pickle.HIGHEST_PROTOCOL)
        with open('best_results.pickle', 'wb') as f:
            pickle.dump(Bayes_Classifier_Best_Length.results, f, pickle.HIGHEST_PROTOCOL)
        with open('best_attr.pickle', 'wb') as f:
            pickle.dump(Bayes_Classifier_Best_Length.totalWords, f, pickle.HIGHEST_PROTOCOL)

    def classify(self, sText):
        '''Given a target string sText, this function returns the most likely document
        class to which the target string belongs. This function should return one of three
        strings: "positive", "negative".

         Calculate the conditional probability of each document class given the features in the target
         document and return the document class of the highest probability

         The conditional probability of a feature f occurring given that a document is of class c is equal to the
         training frequency of feature f in class c divided by the sum of all of frequencies of features in class c.

         The prior probability of a class c is simply equal to the fraction of training documents from class c.
        '''

        global totalDoc
        global totalPositiveFreq
        global totalNegativeFreq
        global totalWords

        # print sText
        sText = sText.lower()
        for r in Bayes_Classifier_Best_Length.results:
            negationFlag = False
            if r == "positive":
                totalFreq = totalPositiveFreq
            else:
                totalFreq = totalNegativeFreq

            priorProb = float(Bayes_Classifier_Best_Length.results[r]) / totalDoc
            if priorProb == 0:
                print "Error Code: 0x334f2"
                priorProb = 1
            condProb = 0
            tokens = self.tokenize(sText)

            if r == "positive":
                length_dict = Bayes_Classifier_Best_Length.positive_length
            else:
                length_dict = Bayes_Classifier_Best_Length.negative_length

            wordCountClassify = len(tokens)
            lengthConditionProb = float(length_dict[wordCountClassify] + 1)/sum(length_dict.values()) + len(length_dict.keys())

            for word in tokens:
                if word in [".", ","]:
                    negationFlag = False
                if word in negationWords:
                    negationFlag = True
                if word in stopWords:
                    continue
                if negationFlag:
                    word = "NOT_" + word
                dictClass = getattr(Bayes_Classifier_Best_Length, r)

                if word in dictClass:
                    ddd = dictClass[word]
                    wordProb = float(dictClass[word] + 1) / (totalFreq + totalWords)
                else:
                    wordProb = float(1) / (totalFreq + totalWords)
                condProb += math.log(wordProb)
            docProb = math.log(priorProb) + condProb + math.log(lengthConditionProb)
            # print "%s: %f" % (r, docProb)
            if r == "positive":
                positive = docProb
            elif r == "negative":
                negative = docProb

        # print positive
        #
        # print negative
        if abs(positive - negative) < 0.05:
            return "neutral"
        elif positive > negative:
            return "positive"
        else:
            return "negative"

    def loadFile(self, sFilename):
        '''Given a file name, return the contents of the file as a string.'''

        f = open(sFilename, "r")
        sTxt = f.read()
        f.close()
        return sTxt

    def save(self, dObj, sFilename):
        '''Given an object and a file name, write the object to the file using pickle.'''

        f = open(sFilename, "w")
        p = pickle.Pickler(f)
        p.dump(dObj)
        f.close()

    def load(self, sFilename):
        '''Given a file name, load and return the object stored in the file.'''

        f = open(sFilename, "r")
        u = pickle.Unpickler(f)
        dObj = u.load()
        f.close()
        return dObj

    def tokenize(self, sText):
        '''Given a string of text sText, returns a list of the individual tokens that
        occur in that string (in order).'''

        lTokens = []
        sToken = ""
        for c in sText:
            if re.match("[a-zA-Z0-9]", str(c)) != None or c == "\'" or c == "_" or c == '-':
                sToken += c
            else:
                if sToken != "":
                    lTokens.append(sToken)
                    sToken = ""
                if c.strip() != "":
                    lTokens.append(str(c.strip()))

        if sToken != "":
            lTokens.append(sToken)

        return lTokens
