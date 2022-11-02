
from repast4py import core
from typing import Tuple, List

from memAlloc import *
from MPIandContext import *


class WinnerLoser(core.Agent):

    TYPE = 0
    
    def __init__(self, local_id: int, rank: int, wallet: float):
        super().__init__(id=local_id, type=WinnerLoser.TYPE, rank=rank)

        self.myWallet = wallet

        self.counterpartRank = -1
        self.counterpartLocalId = -1
        
        self.havePresenceAsSelfOrGhost = [False] * rankNum
        self.havePresenceAsSelfOrGhost[rank] = True
        
    def creatingItsGhostIfAny(self) -> List:
        self.counterpartRank = int(rng.integers(0,rankNum))
        if not self.havePresenceAsSelfOrGhost[self.counterpartRank]:
            self.havePresenceAsSelfOrGhost[self.counterpartRank] = True
            return [self.counterpartRank, ((self.uid[0], self.TYPE, rank), rank)]
    
    # TMP
    def reactingAsGhost(self):
        print("*** in rank",rank,"tick",t(),"ghost",self.uid[0],self.uid[1],self.uid[2],flush=True)


    def save(self) -> Tuple: # mandatory
        """
        Saves the state of the WinnerLoser as a Tuple.

        Returns:
            The saved state of this WinnerLoser.
        """
        return (self.uid, self.myWallet)

    def update(self, wallet: float): # mandatory
        """
        Updates the state of this agent when it is a ghost
        agent on some rank other than its local one.
        """
        self.myWallet=wallet

      
            
def restore_agent(agent_data: Tuple):

    uid=agent_data[0]

    if uid[1] == WinnerLoser.TYPE:
    
        if uid in agent_cache:   # look for agent_cache in model.py
            tmp = agent_cache[uid] # found
            tmp.myWallet = agent_data[1] #restore data

        else: #creation of an instance of the class with its data
            tmp = WinnerLoser(uid[0], uid[2],agent_data[1])                
            agent_cache[uid] = tmp

        return tmp

    
