
agent_cache={} # dict with uid as keys and agents' tuples as values, 
               # used by restore_agent (def in classes.py) to avoid rebuild agents
    
ghostsToRequest=[] # list of tuples containing for each ghost the uid and its current rank;
                   # used by the requestGhosts(self) function of the model
