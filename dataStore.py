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
        with open('wordLists/2020special.csv', newline='') as file:
                reader = csv.reader(file)
                unflattened = list(reader)
                self.data = list(itertools.chain(*unflattened))
                #print(data)
