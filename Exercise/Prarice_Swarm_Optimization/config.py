import numpy as np

from util.formula import rastrigin, rosenbrock, eggholder, ackley

NEIHBORHOOD_TOPOLOGY = 1
ACCELERATION = np.array([1.49618, 1.49618])
INERTIA_W = 0.7298
GENERATION_MAX = 50
MSSV = 18521530
INF = 1e+50

THRESOLD = 0.05

 # default is 0
# 0: Rastrigin
# 1: Rosenbrock
# 2: Eggholder
# 3: Ackley

    
PROBLEM = {
    "Rastrigin":{
        'upper': 5.12,
        "lower": -5.12,
        'formula':rastrigin,
        'optimal_val': 0,
        'thresold': 0.5
    },
    "Rosenbrock": {
        'upper': INF,
        'lower': -INF,
        'formula': rosenbrock,
        'optimal_val': 0,
        'thresold': 25
        
    },
    "Eggholder": {
        "upper": 512,
        'lower': -512,
        'formula':eggholder,
        'optimal_val':-959.6407,
        'thresold': 25
    },
    "Ackley": {
        "upper": 5,
        "lower": -5,
        "formula": ackley,
        'optimal_val': 0,
        'thresold': 0.5
    }
    }

