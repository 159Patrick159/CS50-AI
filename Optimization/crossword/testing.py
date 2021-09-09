import sys
import math
import copy
from typing import Container
from crossword import *

queue = set()
queue.add((1,2))
queue.add((2,3))
queue.add((3,4))
x = {"apple":3,"pears":[4,1],"banana":5,"peach":6}
#a = {word: rank for word, rank in sorted(x.items(), key=lambda item: item[1])}
#b = [word for word in a.keys()]
test = {1:['poopie','stinky'],2:'stinky'}
r = ['book','apple','pear']
if type(test[2]) == str:
    print('poopie')