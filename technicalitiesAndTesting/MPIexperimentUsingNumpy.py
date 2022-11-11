
# https://mpi4py.readthedocs.io/en/stable/tutorial.html#collective-communication "Broadcasting a NumPy array"

from mpi4py import MPI
import numpy as np
import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
rankNum=comm.Get_size()

data=[0]*rankNum

for k in range(rankNum):
    
    if rank == k:
        data[k]=np.array([np.arange(10*k+1,10*k+11),[k]*10] ,dtype='f')
    else:
        data[k]=np.empty([2,10],dtype='f')

    comm.Bcast(data[k], root=k)
    
    print(time.time(),"rank", rank,"\n",data,flush=True)
    
    
