
import time
from mpi4py import MPI
from repast4py import context as ctx
import repast4py 
from repast4py import parameters

comm = MPI.COMM_WORLD
rank    = comm.Get_rank()
rankNum = comm.Get_size() #pt

# create the context to hold the agents and manage cross process
# synchronization
context = ctx.SharedContext(comm)

# https://repast.github.io/repast4py.site/apidoc/source/repast4py.parameters.html
"""
create_args_parser()
Creates an argparse parser with two arguments: 
1) a yaml format file containing model parameter input, and 
2) an optional json dictionary string that can override that input.
"""
parser = parameters.create_args_parser()

args = parser.parse_args()
#print(1,args,flush=True)

"""
init_params(parameters_file, parameters)
Initializes the repast4py.parameters.params dictionary with the model input parameters.
"""
params = parameters.init_params(args.parameters_file, args.parameters)
#print(2,params,flush=True)

repast4py.random.init(rng_seed=params['myRandom.seed'][rank])
rng = repast4py.random.default_rng 

#timer T()
startTime=-1
def T():
    global startTime
    if startTime < 0:
        startTime=time.time()
    return time.time() - startTime



    
