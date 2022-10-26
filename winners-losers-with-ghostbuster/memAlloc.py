
agent_cache={} # dict with uid as keys and agents' tuples as values, 
               # used by restore_agent (def in classes.py) to avoid rebuild agents
               # IS IT IN OUR CASE USEFUL?
    
ghostsToRequest=[] # list of tuples containing for each ghost the uid and its current rank;
                   # used by search function of
                   # GhostBuster class
                   # and by requestGhosts(self) function of the model
