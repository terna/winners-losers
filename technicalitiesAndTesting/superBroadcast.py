
from mpi4py import MPI
import numpy as np
import json

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
rankNum = comm.Get_size()

print("\n"+str(rank)+"/"+str(rankNum))

if rank==0:        # example [0,[0,((0,0,1),1)],[1,((0,1,0),0)],[2]] with rankNum => 3
    mToBcast=[0,[0,((0,0,1),1)],
            [1,((0,1,0),0)]]
    for k in range(2,rankNum):
        mToBcast.append([k])
    #print(mBcast)

if rank!=0:        # example [1|2,[0],[1],[2]] with rankNum -> 3
    mToBcast=[rank]
    for k in range(rankNum):
        mToBcast.append([k])
    #print(mBcast)
    
countB=45+(rankNum-1)*5
str_countB="S"+str(countB)
    
mToBcast=json.dumps(mToBcast)
mToBcast=np.array(mToBcast, dtype=str_countB) #'S80')
mToBcast=mToBcast.tobytes()
print( "before bcast", rank, mToBcast)

data=[""]*rankNum
for k in range(rankNum):
    if rank == k:
        data[k] = mToBcast
    else:
        data[k] = bytearray(countB) #80)
for k in range(rankNum):
    comm.Bcast(data[k], root=k)

for k in range(rankNum):
    data[k]=data[k].decode().rstrip('\x00')

for k in range(rankNum):
    data[k]=json.loads(data[k])

print("\nafter bcast", rank, data)

# collecting for each rank

toRequest=[]

for anItem in data:
        anItem.pop(0)
        for aSubitem in anItem:
            if len(aSubitem)>1 and aSubitem[0]==rank: 
                print(aSubitem)
                if not tuple(aSubitem[1]) in toRequest:
                    toRequest.append(tuple(aSubitem[1]))

print("rank",rank,"requests",toRequest)    
