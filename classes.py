
from repast4py import core
from typing import Tuple, List

from memAlloc import *
from MPIandContext import *


class WinnerLoser(core.Agent):

    TYPE = 0
    
    def __init__(self, local_id: int, rank: int, wallet: float, counterpartRank: int, madeAnExchangeWithGhost: bool):
        super().__init__(id=local_id, type=WinnerLoser.TYPE, rank=rank)

        self.myWallet = wallet

        self.counterpartRank = counterpartRank
        self.counterpartLocalId = -1
        self.madeAnExchangeWithGhost= madeAnExchangeWithGhost
        
        self.havePresenceAsSelfOrGhost = [False] * rankNum
        self.havePresenceAsSelfOrGhost[rank] = True
        
        
    def choosingRankAndCreatingItsGhostIfAny(self) -> List:
        self.counterpartRank = int(rng.integers(0,rankNum))
        if not self.havePresenceAsSelfOrGhost[self.counterpartRank]:
            self.havePresenceAsSelfOrGhost[self.counterpartRank] = True
            return [self.counterpartRank, ((self.uid[0], self.TYPE, rank), rank)]
        
    def operatingInItsRank(self):
        if self.counterpartRank == rank:
            tmpListOfAgentsInTheSameRank = list(context.agents(agent_type=0))
            ii=0
            for i in range(len(tmpListOfAgentsInTheSameRank)):
                if self.uid == tmpListOfAgentsInTheSameRank[i].uid: ii=i
            tmpListOfAgentsInTheSameRank.pop(ii)
            counterpart=tmpListOfAgentsInTheSameRank[int(rng.integers(0,len(tmpListOfAgentsInTheSameRank)))]
            commonWallet = self.myWallet + counterpart.myWallet
            share=float(rng.random())
            self.myWallet = commonWallet*share
            counterpart.myWallet = commonWallet*(1-share)
            #print("rank", rank, "tick", t(), "uid", self.uid,"myWallet",\
            #      self.myWallet, "counterpart", counterpart.uid, "counterpart wallet", counterpart.myWallet, flush = True)
            
        
                              

                    
    # TMP
    def reactingAsGhost(self):
        print("*** in rank",rank,"tick",t(),"ghost",self.uid, self.myWallet, flush=True)
        #pass


    def save(self) -> Tuple: # mandatory
        """
        Saves the state of the WinnerLoser as a Tuple.

        Returns:
            The saved state of this WinnerLoser.
        """
        return (self.uid, (self.myWallet, self.counterpartRank, self.madeAnExchangeWithGhost))

    def update(self, dynState: Tuple): # mandatory
        """
        Updates the state of this agent when it is a ghost
        agent on some rank other than its local one.
        """
        self.myWallet=dynState[0]
        self.counterpartRank = dynState[1]
        self.madeAnExchangeWithGhost = dynState[2]

      
            
def restore_agent(agent_data: Tuple):

    uid=agent_data[0]

    if uid[1] == WinnerLoser.TYPE:
    
        if uid in agent_cache:   # look for agent_cache in model.py
            tmp = agent_cache[uid] # found
            tmp.myWallet = agent_data[1][0] #restore data
            tmp.counterpartRank = agent_data[1][1]
            tmp.madeAnExchangeWithGhost = agent_data[1][2]

        else: #creation of an instance of the class with its data
            tmp = WinnerLoser(uid[0], uid[2],agent_data[1][0], agent_data[1][1], agent_data[1][2])                
            agent_cache[uid] = tmp

        return tmp

    
