
from mpi4py import MPI
from typing import Dict
from repast4py import schedule
from repast4py import context as ctx

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
        
        print(5, "rank", self.rank, "rank number", self.rankNum)
        
        
        # create the context to hold the agents and manage cross process
        # synchronization
        self.context = ctx.SharedContext(comm)
        
        # create the schedule
        # https://repast.github.io/repast4py.site/apidoc/source/repast4py.schedule.html
        
        self.countStep=0
        
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
        self.runner.schedule_repeating_event(0, 1, self.step)
        
        """
        schedule_stop(at)
        Schedules the execution of this schedule to stop at the specified tick.

        Parameters
        at (float) – the tick at which the schedule will stop.
        """
        self.runner.schedule_stop(params['stop.at'])
        
    def step(self):
        
        self.context.synchronize(self.fake)  #???
        
        self.countStep+=1
        
        tick = self.runner.schedule.tick
        
        print("rank",self.rank,"step",self.countStep,"in tick",tick,flush=True)
        
    def fake(self):
        pass
        
    def start(self):
        self.runner.execute()
        
