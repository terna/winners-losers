
from typing import Dict
from model import *

def run(params: Dict):
    #print(3, params)
    #print (4, params['random.seed'])
    #print (4.1, params['a'])
    
    model = Model(MPI.COMM_WORLD, params)
    model.start()
