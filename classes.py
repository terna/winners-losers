
from repast4py import core
from typing import Tuple
from repast4py import context as ctx
from memAlloc import *

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
        
    def save(self) -> Tuple:
        """
        Saves the state of the WinnerLoser as a Tuple.

        Returns:
            The saved state of this Walker.
        """
        return (self.uid, self.myWallet)


        
class Ghostbuster(core.Agent):

    TYPE = 1
    
    def __init__(self, local_id: int, rank: int, context: ctx, prey: Tuple):
        super().__init__(id=local_id, type=Ghostbuster.TYPE, rank=rank)
        
        self.myPrey=prey
        self.context=context
        
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
        if self.context.agent(self.myPrey) == None: 
            print("winnerLoser", self.myPrey, 
                  "not in my rank ("+str(self.uid[2])+")",flush=True)
            
        if (self.myPrey,self.myPrey[2]) not in ghostsToRequestOrUpdate:
            ghostsToRequestOrUpdate.append((self.myPrey,self.myPrey[2]))
                
            
            
def restore_agent(agent_data: Tuple):

    uid=agent_data[0]
    print('qui0', flush=True)
    if uid[1] == WinnerLoser.TYPE:

        if uid in agent_cache:   # look for agent_cache in model.py
            print('qui1', flush=True)
            tmp = agent_cache[uid] # found
            tmp.myWallet = agent_data[1] #restore data

        else: #creation of an instance of the class with its data
            print('qui2', flush=True)
            tmp = WinnerLoser(uid[0], uid[2],agent_data[1])                
            agent_cache[uid] = tmp

        print('qui3', tmp.myWallet,flush=True)
        return tmp
             
    
