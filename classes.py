
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
            print("Not found in my rank",flush=True)
            
            """
            https://repast.github.io/repast4py.site/apidoc/source/repast4py.context.html
            request_agents(requested_agents, create_agent)
            Requests agents from other ranks to be copied to this rank as ghosts.

            This is a collective operation and all ranks must call it, regardless 
            of whether agents are being requested by that rank. The requested agents 
            will be automatically added as ghosts to this rank.

            Parameters
            requested_agents (List) – A list of tuples specifying requested 
            agents and the rank to request from. Each tuple must contain the agents 
            unique id tuple and the rank, for example ((id, type, rank), requested_rank).

            create_agent (Callable) – a Callable that can take the result of an agent 
            save() and return an agent.

            Returns
            The list of requested agents.

            Return type
            List[_core.Agent]
            """
            A=[(self.myPrey,self.myPrey[2])]
            print('A',A,flush=True)
            B=restore_agent
            print('B',B,flush=True)
            C=self.context.request_agents
            print('C',C,flush=True)       
            
            #a=self.context.request_agents([(self.myPrey,self.myPrey[2])],restore_agent)
            a=C(A,B)
            print("Ghost created",a,flush=True)

            
def restore_agent(agent_data: Tuple):
    print("qui",flush=True)
    uid=agent_data[0]
    print (uid,flush=True)
    if uid[1] == WinnerLoser.TYPE:
        if uid in agent_cache:   # look for agent_cache in model.py
            tmp = agent_cache[uid]
        else:
            tmp = WinnerLoser(uid[0], uid[2]) #creation of an instance of the class
            agent_cache[uid] = tmp
        # restore the agent state from the agent_data tuple
        tmp.myWallet = agent_data[1]
        #print('qui', tmp.myWallet)
        return tmp
             
    
