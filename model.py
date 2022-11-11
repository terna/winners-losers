
#from mpi4py import MPI
from MPIandContext import *
from typing import Dict
#from repast4py import schedule
#from repast4py import context as ctx
import repast4py
import json
import csv
import numpy as np
from classes import *
from memAlloc import *
from broadcastF import *



class Model:
    """
    The Model class encapsulates the simulation, and is
    responsible for initialization (scheduling events, creating agents,
    and the grid the agents inhabit IF ANY), and the overall iterating
    behavior of the model.

    Args:
        params: the simulation input parameters
    """
    
    global params
    PARAMS = params
    
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
        runner.schedule_repeating_event(0  , 1, self.counter)
        runner.schedule_repeating_event(0.1, 1, self.agentsChoosingCounterpart)
        runner.schedule_repeating_event(0.2, 1, self.agentsSendingTheirGhosts)      
        runner.schedule_repeating_event(0.3, 1, self.agentsExchangingInTheirRanks)
        runner.schedule_repeating_event(0.4, 1, self.sync)
        runner.schedule_repeating_event(0.5, 1, self.ghostsExchangingInDifferentRanks)
        runner.schedule_repeating_event(0.6, 1,\
                                  self.agentsHavingExchangedWithGhostsPreparingTheirOwnGhosts)
        runner.schedule_repeating_event(0.7, 1, self.agentsSendingTheirGhosts)
        runner.schedule_repeating_event(0.8, 1, self.messengerGhostsReportingOccuredExchanges)
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
            aWallet=1 #10 * rng.random()
            aWinnerLoser = WinnerLoser(i,rank,aWallet,-1,(), 0)
            context.add(aWinnerLoser)
        
            

        
    def counter(self):
        if int(t()) % 100 == 0: print("rank", rank, "tick", t(), flush=True)
    
    def agentsChoosingCounterpart(self):        
        
        del self.mToBcast 
        self.mToBcast = [rank] 
        
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
        
        for aWinnerLoser in context.agents(agent_type=0):
            aRequest = aWinnerLoser.choosingRankAndCreatingItsGhostIfAny()
            if aRequest != None: self.mToBcast.append(aRequest)
    
        print(self.mToBcast, "£££££££££££££££££", rank, t(), flush = True)
        
        
        
    def agentsSendingTheirGhosts(self):
        if not (params['rank_interaction'] or rankNum==1): return     

        broadcastGhostRequests(self.mToBcast, Model.PARAMS, rankNum, rank, comm, ghostsToRequest)  #broadcasting
        
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
        #ic(t(),rank,ghostsToRequest,agent_cache);

        
    def agentsExchangingInTheirRanks(self):
        for aWinnerLoser in context.agents(agent_type=0):
            aWinnerLoser.operatingInItsRank()
  
   
    
    def ghostsExchangingInDifferentRanks(self):          
        if not (params['rank_interaction'] or rankNum==1): return     
        for aWinnerLoser in context.agents(agent_type=0):
            aWinnerLoser.myGhostCounterpartId = ()
        
        del self.mToBcast 
        self.mToBcast = [rank] 
        
        materialsReadyToExchange = list(context.agents(agent_type=0)).copy()     
        if not agent_cache == {}:
            currentGhostList=list(agent_cache.keys())
            for i in range(len(agent_cache)):                
                agent_cache[currentGhostList[i]].actingAsGhost(materialsReadyToExchange)
       
    
    #preparing mToBcast
    def agentsHavingExchangedWithGhostsPreparingTheirOwnGhosts(self):
        if not (params['rank_interaction'] or rankNum==1): return
        for aWinnerLoser in context.agents(agent_type=0):
            if aWinnerLoser.myGhostCounterpartId != ():
                aRequest = aWinnerLoser.sendingMyGhostToConcludeTheExchange()
                if aRequest != None: self.mToBcast.append(aRequest)
        print(self.mToBcast, "$$$$$$$$$$$$$$$$$", rank, t(), flush = True)
        
    
    def messengerGhostsReportingOccuredExchanges(self):
        if not (params['rank_interaction'] or rankNum==1): return
        
        
        materialsToReportTo = list(context.agents(agent_type=0)).copy()     
        if not agent_cache == {}:
            currentReportingGhostList=list(agent_cache.keys())
            for i in range(len(agent_cache)):                
                agent_cache[currentReportingGhostList[i]].actingAsReportingGhost(materialsToReportTo)
    

                    
        
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
        #ic(t(),rank,"synchronisation made");
    
                        
    def finish(self):
        allTheWallets = []
        for aWinnerLoser in context.agents(agent_type=0):
            allTheWallets.append(aWinnerLoser.myWallet)
        
        print("\n\nBye bye by rank",rank,"at tick",t(),"clock",T(),\
              "transaction #", tr(True), flush=True)
        #print(allTheWallets, flush = True)
        
        with open(params["log_file_root"]+str(rank)+'.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(allTheWallets)
                
        
    def start(self):
        runner.execute()
        
