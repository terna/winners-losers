
from repast4py import core
from typing import Tuple
from repast4py import context as ctx

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
        if self.context.agent(self.myPrey) == None: print("Not found in my rank",\
                                                          flush=True)
        
