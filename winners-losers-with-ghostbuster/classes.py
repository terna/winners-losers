
from repast4py import core
from typing import Tuple
#from repast4py import context as ctx
from memAlloc import *
from MPIandContext import *

class WinnerLoser(core.Agent):

    TYPE = 0
    
    def __init__(self, local_id: int, rank: int, wallet: float):
        super().__init__(id=local_id, type=WinnerLoser.TYPE, rank=rank)

        self.myWallet = wallet
        
    def lookForMinWallet(self,agSet):

        agWalletSet=list(aWinnerLoser.myWallet for aWinnerLoser in agSet)
        self.minWalletPosition=agWalletSet.index(min(agWalletSet))
        
    def give(self,agSet):
        
        list(agSet)[self.minWalletPosition].myWallet+=1
        self.myWallet-=1
        
    def save(self) -> Tuple: # mandatory
        """
        Saves the state of the WinnerLoser as a Tuple.

        Returns:
            The saved state of this WinnerLoser.
        """
        print("quiiiiiiiiiiiiiiiiiiiiiiii myWallet", self.myWallet, flush=True)
        return (self.uid, self.myWallet)

    def update(self, wallet: float): # mandatory
        """
        Updates the state of this agent when it is a ghost
        agent on some rank other than its local one.
        """
        self.myWallet=wallet
        print("quaaaaaaaaaaaaaaaaaaaaaaaa", flush=True)

        
class Ghostbuster(core.Agent):

    TYPE = 1
    
    def __init__(self, local_id: int, rank: int, prey: Tuple, ratio: float):
        super().__init__(id=local_id, type=Ghostbuster.TYPE, rank=rank)
        
        self.myPrey=prey
        self.myRatio=ratio

        
    def search(self,tick):
        print("tick",tick,"ghostbuster",self.uid, "searching",self.myPrey,flush=True)
        """
        https://repast.github.io/repast4py.site/apidoc/source/repast4py.context.html
        agent(agent_id)
        Gets the specified agent from the collection of local agents in this context.

        Parameters
        agent_id – the unique id tuple of the agent to return

        Returns
        The agent with the specified id or None if no such agent is found.

        Return type
        _core.Agent
        """
        if context.agent(self.myPrey) == None: 
            print("winnerLoser", self.myPrey, 
                  "not in my rank ("+str(self.uid[2])+")",flush=True)
            
            if (self.myPrey,self.myPrey[2]) not in ghostsToRequest:  
                ghostsToRequest.append((self.myPrey,self.myPrey[2]))
            
    def lookAtGhostWallets(self,tick,rank):
        
        if context.ghost_agent(self.myPrey) != None:
            print("tick",tick,"rank",rank, "the ghost",\
                  context.ghost_agent(self.myPrey),\
                  "has wallet",context.ghost_agent(self.myPrey).myWallet,flush=True)

 
    def save(self) -> Tuple: # mandatory
        """
        Saves the state of the WinnerLoser as a Tuple.

        Returns:
            The saved state of this WinnerLoser.
        """
        print("quIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII myPrey", self.myPrey, flush=True)
        # The first element of this full state tuple is the agent’s unique id, 
        # itself a tuple (accessed via the uid attribute), and the 
        # second is the dynamic state of that agent. 
        return (self.uid, (self.myPrey, self.myRatio))

    def update(self, dynState: Tuple): #prey: Tuple, ratio: float): # mandatory
        # look at row 239 of context.py
        """
        Updates the state of this agent when it is a ghost
        agent on some rank other than its local one.
        """
        self.myPrey=dynState[0] #prey # useful if the prey changes
        self.myRatio=dynState[1] #ratio
        #self.myContext=context
        print("quAAAAAAAAAAAAAAAAAAAAAAAAA", flush=True)
            
            
def restore_agent(agent_data: Tuple):

    uid=agent_data[0]

    if uid[1] == WinnerLoser.TYPE:
        print("quoooooooooooooooooooooooooooo", flush=True)
    
        if uid in agent_cache:   # look for agent_cache in model.py
            tmp = agent_cache[uid] # found
            tmp.myWallet = agent_data[1] #restore data

        else: #creation of an instance of the class with its data
            tmp = WinnerLoser(uid[0], uid[2],agent_data[1])                
            agent_cache[uid] = tmp

        return tmp
             
    if uid[1] == Ghostbuster.TYPE:
        print("quOOOOOOOOOOOOOOOOOOOOOOOOOOOOO", flush=True)
    
        if uid in agent_cache:   # look for agent_cache in model.py
            tmp = agent_cache[uid] # found
            tmp.myPrey = agent_data[1][0] #restore data
            tmp.myRatio = agent_data[1][1] #restore data
            #tmp.myContext = agent_data[2] #restore data

        else: #creation of an instance of the class with its data
            tmp = Ghostbuster(uid[0], uid[2],agent_data[1][0],agent_data[1])  
            agent_cache[uid] = tmp

        return tmp
    
