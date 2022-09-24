
from repast4py import core
from typing import Tuple

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
    
    def __init__(self, local_id: int, rank: int, prey: Tuple):
        super().__init__(id=local_id, type=Ghostbuster.TYPE, rank=rank)
        
        self.myPrey=prey
