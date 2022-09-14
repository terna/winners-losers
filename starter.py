
from repast4py import parameters
from runMod import *

# https://repast.github.io/repast4py.site/apidoc/source/repast4py.parameters.html
"""
create_args_parser()
Creates an argparse parser with two arguments: 
1) a yaml format file containing model parameter input, and 
2) an optional json dictionary string that can override that input.
"""
parser = parameters.create_args_parser()

args = parser.parse_args()
print(1,args,flush=True)

"""
init_params(parameters_file, parameters)
Initializes the repast4py.parameters.params dictionary with the model input parameters.
"""
params = parameters.init_params(args.parameters_file, args.parameters)
print(2,params,flush=True)

run(params)
