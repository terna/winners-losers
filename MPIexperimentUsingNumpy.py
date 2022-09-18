
# MPIexperimentUsingNumpy.py

import numpy as np
import random
from mpi4py import MPI

comm = MPI.COMM_WORLD
procid = comm.Get_rank()
nprocs = comm.Get_size()
if nprocs<2:
    print("C'mon, get real....")
    sys.exit(1)

random.seed(procid)
random_bound = nprocs*nprocs
random_number = random.randint(1,random_bound)
#print("[%d] random=%d" % (procid,random_number),flush=True)

# native mode send
#print("a",procid,random_number,flush=True)
max_random = comm.allreduce(random_number,op=MPI.MAX) # max over all procid
#print("b",procid,max_random,flush=True)

if procid==0:
    print("Python native:\n max=%d" % max_random,flush=True)

myrandom = np.empty(1,dtype=int) #unitilized
myrandom[0] = random_number
allrandom = np.empty(nprocs,dtype=int)

# numpy mode send
comm.Allreduce(myrandom,allrandom[:1],op=MPI.MAX)
print(procid,allrandom,flush=True)

if procid==0:
    print("Python numpy:\n max=%d" % allrandom[0],flush=True)
