# Link of formula: https://en.wikipedia.org/wiki/Test_functions_for_optimization

import numpy as np

def rastrigin(X):
    # arg: + n is dimension of data 
    #        X is vector
    # 
    return 10*len(X) + np.sum(X**2 + 10*np.cos(2*np.pi*X))
 

def rosenbrock(X):
    sum = 0 
    for i in range(len(X)-1):
        sum += 100*(X[i+1] - X[i]**2)**2 + (1-X[i])**2
    return sum

def eggholder(X):
    return -(X[1] + 47)*np.sin(np.sqrt(np.abs(X[0]/2 + X[1] + 47 ))) \
        - (X[0]*np.sin(np.sqrt(np.abs(X[0]- (X[1] + 47)))))

def ackley(X):
    return -20*np.exp(-0.2*np.sqrt(0.5*(X[0]**2 + X[1]**2))) \
        - np.exp(0.5*(np.cos(2*np.pi*X[0]) + np.cos(2*np.pi*X[1]))) + np.e + 20