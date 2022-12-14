
from repast4py import core
from typing import Tuple, List

from memAlloc import *
from MPIandContext import *

class WinnerLoser(core.Agent):

    TYPE = 0
    
    def __init__(self, local_id: int, rank: int, wallet: float, counterpartRank: int,\
                myGhostCounterpartId: Tuple, materialWalletValueToBeReported: float):
        super().__init__(id=local_id, type=WinnerLoser.TYPE, rank=rank)

        self.myWallet = wallet

        self.counterpartRank = counterpartRank
        self.counterpartLocalId = -1
        
        self.havePresenceAsSelfOrGhost = [False] * rankNum
        self.havePresenceAsSelfOrGhost[rank] = True
        
        self.myGhostCounterpartId = myGhostCounterpartId
        
        self.materialWalletValueToBeReported = materialWalletValueToBeReported
        
        self.movAvElements = []
        
        
    def movAv(self,x):
        
        self.movAvElements.append(x)
        if len(self.movAvElements) > params['movAvElementNum']: self.movAvElements.pop(0)
        
    def choosingRankAndCreatingItsGhostIfAny(self) -> List:
        if params['rank_interaction']: self.counterpartRank = int(rng.integers(0,rankNum))
        else:                          self.counterpartRank = rank
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
            self.movAv(self.myWallet)
            counterpart.myWallet = commonWallet*(1-share)
            counterpart.movAv(counterpart.myWallet)
            tr()
            
        
                              
    def actingAsGhost(self, materialsReadyToExchange):
        if materialsReadyToExchange == []: return #maybe unuseful
        if self.counterpartRank==rank: 
                           # the choice of the WL sending the ghost is to op. here
                           # maybe, the WL has also ghosts in other ranks
            materialCounterpart = materialsReadyToExchange.pop(int(rng.integers(0,len(materialsReadyToExchange))))
            commonWallet = self.myWallet + materialCounterpart.myWallet
            share=float(rng.random())
            self.myWallet = commonWallet*share 
                           # the ghost wallet, not relevant
            self.movAv(self.myWallet) #?????
            materialCounterpart.materialWalletValueToBeReported = self.myWallet
                           # the wallet to be reported the WL sending the ghost
                           # in the while, also the movAa() f. will be activated
            materialCounterpart.myWallet = commonWallet*(1-share)
            materialCounterpart.movAv(materialCounterpart.myWallet)
                           # the counterpart wallet
            tr()
            
            materialCounterpart.myGhostCounterpartId = self.uid
            #print("@@@@@@@", materialCounterpart.myGhostCounterpartId, materialCounterpart)
    
    
    def actingAsReportingGhost(self, materialsToReportTo):
        if materialsToReportTo == []: return #maybe unuseful
        if self.myGhostCounterpartId == (): return #because it is not a reportingGhost(messenger)
        
        notFound = True
        i = 0
        while notFound: 
            if materialsToReportTo[i].uid == self.myGhostCounterpartId:
                #print("FOUND", rank, t(), materialsToReportTo[i].uid,\
                #      self.myGhostCounterpartId, self.materialWalletValueToBeReported,\
                #      self.myWallet, flush =True)
                notFound = False
                materialsToReportTo[i].myWallet = self.materialWalletValueToBeReported
                materialsToReportTo[i].movAv(self.materialWalletValueToBeReported)
            else: 
                i+=1
                if i == len(materialsToReportTo): return

                
            
    def sendingMyGhostToConcludeTheExchange(self) -> List:

        #return [self.uid[2], (self.uid, self.uid[2])]
        #return [self.myGhostCounterpartId[2], (self.myGhostCounterpartId, self.myGhostCounterpartId[2])]
        return [self.myGhostCounterpartId[2], (self.uid, self.uid[2])]
               # sending a ghost from myself to the rank from where the counterpart ghost
               # was coming

        
     

    def save(self) -> Tuple: # mandatory
        """
        Saves the state of the WinnerLoser as a Tuple.

        Returns:
            The saved state of this WinnerLoser.
        """
        return (self.uid, (self.myWallet, self.counterpartRank, self.myGhostCounterpartId, \
                           self.materialWalletValueToBeReported))

    def update(self, dynState: Tuple): # mandatory
        """
        Updates the state of this agent when it is a ghost
        agent on some rank other than its local one.
        """
        self.myWallet=dynState[0]
        self.counterpartRank = dynState[1]
        self.myGhostCounterpartId = dynState[2]
        self.materialWalletValueToBeReported = dynState[3]

      
            
def restore_agent(agent_data: Tuple):
    
    uid=agent_data[0]

    if uid[1] == WinnerLoser.TYPE:
    
        if uid in agent_cache:   # look for agent_cache in model.py
            tmp = agent_cache[uid] # found
            tmp.myWallet = agent_data[1][0] #restore data
            tmp.counterpartRank = agent_data[1][1]
            tmp.myGhostCounterpartId = agent_data[1][2]
            tmp.materialWalletValueToBeReported = agent_data[1][3]


        else: #creation of an instance of the class with its data
            tmp = WinnerLoser(uid[0], uid[2],agent_data[1][0], agent_data[1][1],\
                             agent_data[1][2], agent_data[1][3])                
            agent_cache[uid] = tmp

        return tmp

    
