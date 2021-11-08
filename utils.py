from math import sqrt

def calculate_std_dev(collection, mean):
    return sqrt(sum(list(map(lambda k: (k-mean)**2, collection)))/(len(collection)-1))

def calculate_variance(collection, mean):
    return sum(list(map(lambda k: (k-mean)**2, collection)))/(len(collection)-1)