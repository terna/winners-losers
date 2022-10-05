
from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

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
