# -*- coding: utf-8 -*-
#Activity Online - an online guessing game
#Copyright (C) 2021 Peter Munk

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU Affero General Public License as
#published by the Free Software Foundation, either version 3 of the
#License, or (at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU Affero General Public License for more details.

#You should have received a copy of the GNU Affero General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.

import csv
import random
import itertools
import os
import datetime 
import re
import copy 

wordPath = 'wordLists/'
uploaded = 'uploadedWordLists/'

class DataStore:

    data = []
    dataOrg = []
    wordListSet = []
    hasOwnWords = False
    
    def isEmpty(self):
        return not self.data
    
    def getRandomElement(self):
        if not self.data:
           return "[Empty]"
        else:
            element = random.choice(self.data)
            self.data.remove(element)
            #print(element)
            return element

    def reset(self):
        self.data = copy.deepcopy(self.dataOrg)
            
    def loadWordSets(self, wordListSet):
        if wordListSet:
            self.wordListSet = wordListSet
            self.data = []
            for wordList in self.wordListSet:
                try:
                    with open(wordPath+wordList+'.csv', newline='', encoding='utf-8') as file:
                        reader = csv.reader(file)
                        unflattened = list(reader)
                        self.data.extend(list(itertools.chain(*unflattened)))
                except IOError:
                    print(wordPath+wordList+'.csv does not exist')
            self.dataOrg = copy.deepcopy(self.data)
            #print("word lists loaded: "+format(self.data))

    def parseCustomWordList(self, wordList):
        self.data = []
        self.data.extend(re.split('[:,;\n]{1}', wordList))
        self.dataOrg = copy.deepcopy(self.data)
        self.hasOwnWords = True
        #print("own word list loaded: "+format(self.data))
        
    def getWordLists(self):
        return self.wordListSet
        
    def usesOwnWord(self):
        return self.hasOwnWords
        
    def getAvailableLists():
        availFiles = {}
        for file in os.listdir(wordPath):
            availFiles[file[:len(file)-4]] = len(open(wordPath+file).readlines(  ))
        return availFiles
        
    def saveCustomWordList(wordList, roomName):
        try:
            fileName = uploaded+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-")+roomName+".csv"
            csv_file = open(fileName, "wt", newline='',  encoding='utf-8')
            csv_file.write(wordList)
            csv_file.close()
        except IOError:
            print('Could not create file'+fileName)
