
import time
from mpi4py import MPI
from repast4py import context as ctx
import repast4py 
from repast4py import parameters

# simple debug
from icecream import ic

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


"""
init_params(parameters_file, parameters)
Initializes the repast4py.parameters.params dictionary with the model input parameters.
"""
params = parameters.init_params(args.parameters_file, args.parameters)

"""
repast4py.random.default_rng: numpy.random._generator.Generator = Generator(PCG64) 
at 0x7F6812E0CD60 repast4py’s default random generator created using init. 
See the Generator API documentation for more information on the available distributions 
and sampling functions.

Type
numpy.random.Generator

repast4py.random.init(rng_seed=None)
Initializes the default random number generator using the specified seed.

Parameters
rng_seed (int) – the random number seed. Defaults to None in which case, the current 
time as returned by time.time() is used as the seed.
"""

repast4py.random.init(rng_seed=params['myRandom.seed'][rank])
rng = repast4py.random.default_rng 



#timer T()
startTime=-1
def T():
    global startTime
    if startTime < 0:
        startTime=time.time()
    return time.time() - startTime



    
