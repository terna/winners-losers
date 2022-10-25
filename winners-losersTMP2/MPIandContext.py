
import time
from mpi4py import MPI
from repast4py import context as ctx

comm = MPI.COMM_WORLD
rank    = comm.Get_rank()
rankNum = comm.Get_size() #pt

# create the context to hold the agents and manage cross process
# synchronization
context = ctx.SharedContext(comm)

#timer T()
startTime=-1
def T():
    global startTime
    if startTime < 0:
        startTime=time.time()
    return time.time() - startTime
    
