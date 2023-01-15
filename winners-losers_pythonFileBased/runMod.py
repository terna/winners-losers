
from typing import Dict
from model import *

def run(params: Dict):
    
    model = Model(params) #Model(MPI.COMM_WORLD, params)
    model.start()
