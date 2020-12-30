#(c) Peter Munk 2020

import csv
import random
import itertools

class DataStore:

    data = []

    def __init__(self):
        self.reset()
    
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
        with open('testWords.csv', newline='') as file:
                reader = csv.reader(file)
                unflattened = list(reader)
                self.data = list(itertools.chain(*unflattened))
                #print(data)
