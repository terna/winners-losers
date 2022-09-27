
from mpi4py import MPI
from typing import Dict
from repast4py import schedule
from repast4py import context as ctx
import repast4py
import time
"""
time() -> floating point number
        Return the current time in seconds since the Epoch.
        Fractions of a second may be present if the system clock provides them.
to know the Epoch, time.gmtime(0) (in Unix: 19700101)
"""
from classes import *

agent_cache={} # dict with uid as keys and agents' tuples as values, 
               # used by restore_agent (def in classes.py)

class Model:
    """
    The Model class encapsulates the simulation, and is
    responsible for initialization (scheduling events, creating agents,
    and the grid the agents inhabit IF ANY), and the overall iterating
    behavior of the model.

    Args:
        comm: the mpi communicator over which the model is distributed.
        params: the simulation input parameters
    """
    def __init__(self, comm: MPI.Intracomm, params: Dict):

        self.rank    = comm.Get_rank()
        self.rankNum = comm.Get_size() #pt
        
        #print(5, "rank", self.rank, "rank number", self.rankNum)
        
        
        # create the context to hold the agents and manage cross process
        # synchronization
        self.context = ctx.SharedContext(comm)
        
        # create the schedule
        # https://repast.github.io/repast4py.site/apidoc/source/repast4py.schedule.html
                
        """
        init_schedule_runner(comm)
        Initializes the default schedule runner, a dynamic schedule of executable 
        events shared and synchronized across processes.
        Events are added to the scheduled for execution at a particular tick. 
        The first valid tick is 0. Events will be executed in tick order, earliest 
        before latest. Events scheduled for the same tick will be executed in the 
        order in which they were added. If during the execution of a tick, 
        an event is scheduled before the executing tick (i.e., scheduled to occur in 
        the past) then that event is ignored. The scheduled is synchronized across 
        process ranks by determining the global cross-process minimum next scheduled 
        event time, and executing only the events schedule for that time. In this way, 
        no schedule runs ahead of any other.
        """
        self.runner = schedule.init_schedule_runner(comm)
        
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
        self.runner.schedule_repeating_event(0, 1, self.lookAtWalletsAndGive)
        self.runner.schedule_repeating_event(0.1, 1, self.activateGhostbusters)
        
        """
        schedule_stop(at)
        Schedules the execution of this schedule to stop at the specified tick.

        Parameters
        at (float) – the tick at which the schedule will stop.
        """
        self.runner.schedule_stop(params['stop.at'])
        
        self.runner.schedule_end_event(self.finish)
        

        
        # create agents
        
        # https://repast.github.io/repast4py.site/apidoc/source/repast4py.random.html
        """
        Random numbers for repast4py. When this module is imported, 
        repast4py.random.default_rng is created using the current epoch time as 
        the random seed, and repast4py.random.seed is set to that value. 
        
        repast4py.random.init(rng_seed=None)
        Initializes the default random number generator using the specified seed.
        """
        repast4py.random.init(rng_seed=params['myRandom.seed'][self.rank])
        rng = repast4py.random.default_rng 
        
        # winnerLoser agents
        
        for i in range(params['WinnerLoser.count'] // self.rankNum): 
                                                #to subdivide the total #pt
            # create and add the agent to the context
            aWallet=10 * rng.random()
            #print(aWallet,flush=True)
            aWinnerLoser = WinnerLoser(i,self.rank,aWallet)
            self.context.add(aWinnerLoser)
            
        # ghostbuster agents
  
        if self.rank==0:
            aGhostbuster = Ghostbuster(0,self.rank,self.context,(0,0,1))
            self.context.add(aGhostbuster) 
            
        
    def lookAtWalletsAndGive(self):
        
        """
        NOT NECESARY IF NO PROJECTIONS
        synchronize(restore_agent, sync_ghosts=True)
        Synchronizes the model state across processes by moving agents, 
        filling projection buffers with ghosts, updating ghosted state and so forth.

        Parameters
        restore_agent (Callable) – a callable that takes agent state data and 
        returns an agent instance from that data. The data is a tuple whose first 
        element is the agent’s unique id tuple, and the second element is the 
        agent’s state, as returned by that agent’s type’s save() method.

        sync_ghosts (bool) – if True, the ghosts in any SharedProjections and 
        value layers associated with this SharedContext are also synchronized. 
        Defaults to True.
        """
                
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

        tick = self.runner.schedule.tick        
        print("rank",self.rank,"at tick",tick,"clock",time.time(),\
                            "\nwallets",list(aWinnerLoser.myWallet\
                            for aWinnerLoser in self.context.agents(agent_type=0)),\
                            flush=True)
                
        for aWinnerLoser in self.context.agents(agent_type=0):
            aWinnerLoser.lookForMinWallet(self.context.agents(agent_type=0))
            
            aWinnerLoser.give(self.context.agents(agent_type=0))
            
    def activateGhostbusters(self):
        tick = self.runner.schedule.tick

        """
        https://repast.github.io/repast4py.site/apidoc/source/repast4py.context.html
        
        size(agent_type_ids=None)
        Gets the number of local agents in this SharedContext, optionally by type.

        Parameters
        agent_type_ids (List[int]) – a list of the agent type ids identifying the 
        agent types to count. If this is None then the total size is returned with 
        an agent type id of -1.

        Returns
        A dictionary containing the counts (the dict values) by agent type (the 
        dict keys).

        Return type
        dict

        """

        atype_id = 1
        # _agents_by_type from Nick mail 20220926
        has_type = True if atype_id in self.context._agents_by_type and\
                   len(self.context._agents_by_type[atype_id]) > 0 else False
        if has_type:
            for aGhostbuster in self.context.agents(agent_type=1):  
                aGhostbuster.search(tick)
                
    def finish(self):
        tick = self.runner.schedule.tick
        print("ciao by rank",self.rank,"at tick",tick,"clock",time.time(),flush=True)
        
    def start(self):
        self.runner.execute()
        
