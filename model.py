
#from mpi4py import MPI
from MPIandContext import *
from typing import Dict
#from repast4py import schedule
#from repast4py import context as ctx
import repast4py
import json
import numpy as np
from classes import *
from memAlloc import *

def countDigits(n):
    count = 0
    while(n>0):
        count+=1
        n=n//10
    return count


class Model:
    """
    The Model class encapsulates the simulation, and is
    responsible for initialization (scheduling events, creating agents,
    and the grid the agents inhabit IF ANY), and the overall iterating
    behavior of the model.

    Args:
        params: the simulation input parameters
    """
    def __init__(self, params: Dict):

        
        self.mToBcast = []
        
        # the context to hold the agents and manage cross process synchronization
        # is created in step -2

        
        # the runner, implementing the schedule, is created in step -2
        # https://repast.github.io/repast4py.site/apidoc/source/repast4py.schedule.html
        
        """
        schedule_repeating_event(at, interval, evt)
        Schedules the specified event to execute at the specified tick, and repeat at 
        the specified interval.

        Parameters
        at (float) – the time of the event.
        interval (float) – the interval at which to repeat event execution.
        evt (Callable) – the Callable to execute when the event occurs.

            A callable is anything that can be called.
            The built-in callable (PyCallable_Check in objects.c) checks if the argument 
            is either:
                an instance of a class with a __call__ method or
                is of a type that has a non null tp_call (c struct) member which 
                indicates callability otherwise (such as in functions, methods etc.)
        """
        runner.schedule_repeating_event(0, 1, self.agentsChoosingCounterpart)
        runner.schedule_repeating_event(0.3, 1, self.sync)
        
        """
        schedule_stop(at)
        Schedules the execution of this schedule to stop at the specified tick.

        Parameters
        at (float) – the tick at which the schedule will stop.
        """
        runner.schedule_stop(params['stop.at'])
        
        runner.schedule_end_event(self.finish)
        

        
        # create agents
        # winnerLoser agents
        
        for i in range(params['WinnerLoser.count'] // rankNum): 
                                                #to subdivide the total #pt
            # create and add the agent to the context
            aWallet=10 * rng.random()
            aWinnerLoser = WinnerLoser(i,rank,aWallet)
            context.add(aWinnerLoser)
            

        
    def agentsChoosingCounterpart(self):        
        
        """
        agents(agent_type=None, count=None, shuffle=False)
        Gets the agents in this SharedContext, optionally of the specified type, count 
        or shuffled.

        Parameters
        agent_type (int) – the type id of the agent, defaults to None.
        count (int) – the number of agents to return, defaults to None, meaning return 
        all the agents.shuffle (bool) – whether or not the iteration order is shuffled.
        If true, the order is shuffled. If false, the iteration order is the order of 
        insertion.

        Returns
        An iterable over all the agents in the context. If the agent_type is 
        not None then an iterable over agents of that type will be returned.

        Return type
        iterable 
        pt addendum: it is a generator, not a list
        """
        
        del self.mToBcast 
        self.mToBcast = [rank] 
        
        for aWinnerLoser in context.agents(agent_type=0):
            aRequest = aWinnerLoser.requestingGhostIfAny()
            if aRequest != None: self.mToBcast.append(aRequest)
    
        ic(t(),self.mToBcast);
        self.requestGhosts()
           
        
    def requestGhosts(self): 
       
        n=params['WinnerLoser.count'] // rankNum
        countB = 10+n*(22+countDigits(n))
        str_countB="S"+str(countB)
            
        self.mToBcast=json.dumps(self.mToBcast)
        self.mToBcast=np.array(self.mToBcast, dtype=str_countB) 
        self.mToBcast=self.mToBcast.tobytes()    
        
        data=[""]*rankNum
        for k in range(rankNum):
            if rank == k:
                data[k] =self.mToBcast
            else:
                data[k] = bytearray(countB) 
        for k in range(rankNum):
            comm.Bcast(data[k], root=k)

        for k in range(rankNum):
            data[k]=data[k].decode().rstrip('\x00')

        for k in range(rankNum):
            data[k]=json.loads(data[k])
            

        for anItem in data:
            anItem.pop(0)
            for aSubitem in anItem: 
                if len(aSubitem)>1 and aSubitem[0]==rank: 
                    aaSubitem = aSubitem[1][0]
                    aaSubitem = tuple(aaSubitem)
                    aSubitem=(aSubitem[0], (aaSubitem, aSubitem[1][1]))
                    
                    if not tuple(aSubitem[1]) in ghostsToRequest:
                        ghostsToRequest.append(tuple(aSubitem[1]))
        
        
        """
        https://repast.github.io/repast4py.site/apidoc/source/repast4py.context.html
        request_agents(requested_agents, create_agent)
        Requests agents from other ranks to be copied to this rank as ghosts.

        !!!! This is a collective operation and all ranks must call it, regardless 
        of whether agents are being requested by that rank. The requested agents 
        will be automatically added as ghosts to this rank.

        Parameters
        requested_agents (List) – A list of tuples specifying requested 
        agents and the rank to request from. Each tuple must contain the agents 
        unique id tuple and the rank, for example ((id, type, rank), requested_rank).

        create_agent (Callable) – a Callable that can take the result of an agent 
        save() and return an agent.

        Returns
        ***The list of requested agents.

        Return type
        List[_core.Agent]
        """
        context.request_agents(ghostsToRequest,restore_agent)
        ic(t(),rank,ghostsToRequest,agent_cache);
        

        
    def sync(self):
        """
        synchronize(restore_agent, sync_ghosts=True)
        Synchronizes the model state across processes by moving agents, 
        filling projection buffers with ghosts, updating ghosted state and so forth.

        Parameters
        restore_agent (Callable) – a callable that takes agent state data and returns 
        an agent instance from that data. The data is a tuple whose first element 
        is the agent’s unique id tuple, and the second element is the agent’s state, 
        as returned by that agent’s type’s save() method.

        sync_ghosts (bool) – if True, the ghosts in any SharedProjections and 
        value layers associated with this SharedContext are also synchronized. 
        Defaults to True.
        """
        context.synchronize(restore_agent)
        ic(t(),rank,"synconisation made");
    
                        
    def finish(self):
        print("\n\nBye bye by rank",rank,"at tick",t(),"clock",T(),flush=True)
        
    def start(self):
        runner.execute()
        
