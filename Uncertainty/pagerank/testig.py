import numpy as np
from numpy.core.fromnumeric import mean
from numpy.lib.function_base import average

corpus = {'foo':['a','b','c']}
l = [link for link in corpus['foo']]
print(l)