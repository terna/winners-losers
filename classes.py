
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

    
