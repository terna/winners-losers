
import json
import numpy as np



def countDigits(n):
    count = 0
    while(n>0):
        count+=1
        n=n//10
    return count

def broadcastGhostRequests(mToBcast, params, rankNum, rank, comm, ghostsToRequest):
    
    n=params['WinnerLoser.count'] // rankNum
    countB = 10+n*(22+countDigits(n))
    str_countB="S"+str(countB)
            
    mToBcast=json.dumps(mToBcast)
    mToBcast=np.array(mToBcast, dtype=str_countB) 
    mToBcast=mToBcast.tobytes()    
        
    data=[""]*rankNum
    for k in range(rankNum):
        if rank == k:
            data[k] =mToBcast
        else:
            data[k] = bytearray(countB) 
    for k in range(rankNum):
        comm.Bcast(data[k], root=k)

    for k in range(rankNum):
        data[k]=data[k].decode().rstrip('\x00')

    for k in range(rankNum):
        data[k]=json.loads(data[k])
            

    for anItem in data:
        anItem.pop(0)
        for aSubitem in anItem: 
            if len(aSubitem)>1 and aSubitem[0]==rank: 
                aaSubitem = aSubitem[1][0]
                aaSubitem = tuple(aaSubitem)
                aSubitem=(aSubitem[0], (aaSubitem, aSubitem[1][1]))
                    
                if not tuple(aSubitem[1]) in ghostsToRequest:
                    ghostsToRequest.append(tuple(aSubitem[1]))
                    
