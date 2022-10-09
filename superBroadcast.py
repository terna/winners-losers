
from mpi4py import MPI
import numpy as np
import json

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
rankNum = comm.Get_size()

print("\n"+str(rank)+"/"+str(rankNum))

if rank==0:              # example [0,[0,((0,0,1),1)],[1,((0,1,0),0)],[2]] with rankNum => 3
    mToBcast=[0,[0,((0,0,1),1)],
            [1,((0,1,0),0)]]
    for k in range(2,rankNum):
        mToBcast.append([k])
    #print(mBcast)

if rank!=0:              # example [1|2,[0],[1],[2]] with rankNum -> 3
    mToBcast=[rank]
    for k in range(rankNum):
        mToBcast.append([k])
    #print(mBcast)
    
mToBcast=json.dumps(mToBcast)
mToBcast=np.array(mToBcast, dtype='S50')
mToBcast=mToBcast.tobytes()
print( "before bcast", rank, mToBcast)

data=[""]*rankNum
for k in range(rankNum):
    if rank == k:
        data[k] = mToBcast
    else:
        data[k] = bytearray(50)
for k in range(rankNum):
    comm.Bcast(data[k], root=k)

#print("\nafter bcast", rank, data)

for k in range(rankNum):
    data[k]=data[k].decode().rstrip('\x00')
    
#print("\nafter bcastII", rank, data)

#for k in range(rankNum):
#    print(type(data[k]))

for k in range(rankNum):
    data[k]=json.loads(data[k])

print("\nafter bcastIII", rank, data)

    

"""
data=np.frombuffer(data, dtype='S50', count=1)
data = data.reshape((1,1))

print("\n",rank, data,"\n")
"""

"""
print(mToBcast)
print(type(mToBcast),len(mToBcast))
if rank==0:
    print(json.loads(mToBcast))
"""
    
"""
myMa = [['zzz', '2', '-1'], ['xxx', '5', '-99'], ['zzzabcdefghilmn', '2', '-1']]
myMa_arr = np.array(myMa, dtype='S10')
myMa_arr_b = myMa_arr.tobytes()

if rank == 0:
    data = myMa_arr_b
else:
    data = bytearray(90)

comm.Bcast(data, root=0)

data=np.frombuffer(data, dtype='S10', count=9)
data = data.reshape((3, 3))
print(rank, data)
"""
