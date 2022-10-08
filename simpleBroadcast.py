
from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

myMa1 = [['1zzz', '2', '-1'], ['xxx', '5', '-99'], ['zzzabcdefghilmn', '2', '-1']]
myMa1_arr = np.array(myMa1, dtype='S10')
myMa1_arr_b = myMa1_arr.tobytes()

if rank == 1:
    data1 = myMa1_arr_b
else:
    data1 = bytearray(90)

comm.Bcast(data1, root=1)

data1=np.frombuffer(data1, dtype='S10', count=9)
data1 = data1.reshape((3, 3))
print(rank, data1)
print(rank, data1[0,0].decode("utf-8") )


myMa2 = [['2zzz', '2', '-1'], ['xxx', '5', '-99'], ['zzzabcdefghilmn', '2', '-1']]
myMa2_arr = np.array(myMa2, dtype='S10')
myMa2_arr_b = myMa2_arr.tobytes()

if rank == 2:
    data2 = myMa2_arr_b
else:
    data2 = bytearray(90)

comm.Bcast(data2, root=2)

data2=np.frombuffer(data2, dtype='S10', count=9)
data2 = data2.reshape((3, 3))
print(rank, data2)
print(rank, data2[0,0].decode("utf-8") )
