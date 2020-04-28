'''
File name: mpt.py
    Multi Process Task (MPT) class implementation.
           
Author: Vasileios Saveris
email: vsaveris@gmail.com

License: MIT

Date last modified: 15.04.2020

Python Version: 3.8
'''

# My packages
import utils as ut

# Python packages
import time
from multiprocessing import Pool


class MPT():
    '''
    Multi Process Task (MPT) class implementation.
    
    The MPT object creates multiple python processes for executing in parallel a 
    given task for an iteratable collection. The number of processes, the 
    iteratable, the task and the input arguments for the task are given as input 
    parameters.

    Args:
        iteratable (iteratable): An iteratable object. The task has to be 
            executed for each member of the iteretable. Each member of the
            iteratable is the first argument of the task. The rest arguments
            of the task are taken from the **kwargs argument (see below).
            
        task (object): The task to be executed for each member of the iteratable.
            It should be a function call.
            
        processes (int): The number of processes to be used. If None, then the
            created processes are equal to the number of the available cpu cores.
        
        verbose (boolean, default is False): If True print services are enabled.
        
        **kwargs (dictionary): The arguments to be passed on each task call.
            The call to each task should be task(member, **kwargs), where member
            is each member of the iteratable.

    Public Attributes:
        -
        
    Private Attributes:
        See constructor (self._*)
                                
    Public Methods:
        
        execute (args) -> list: Executes the task for the input arguments. It 
            returns a list of objects returned by each task execution.
        
    Private Methods:
        -
        
    Raises:
        -
        
    '''

    def __init__(self, iteratable, task, processes = None, verbose = False, 
        **kwargs):
        
        self._verbose = verbose
        
        if self._verbose:
            print('- Multi Process Task initialization: ', 
                ut.formatArguments(locals().items(), ['self', 'iteratable', 
                'verbose', 'kwargs']), ', number of tasks = ', len(iteratable),
                sep = '', end = '', flush = True)
        
        self._processes = processes
        self._iteratable = iteratable
        self._task = task
        self._kwargs = kwargs
                
    
    def execute(self):
        '''
        Executes a task for each member of an iteratable using a process pool
    
        Args:
            -

        Raises:
            -

        Returns:
            list: A list of objects returned by each task execution. 
        '''
        
        # Start measuring execution time
        start_time = time.time()
        
        # Pool of processes
        processes_pool = Pool(self._processes)
        
        # Execute the task for each member of the iteratable
        results = [processes_pool.apply_async(self._task, (i, self._kwargs,))
            for i in self._iteratable]
        
        processes_pool.close()
        processes_pool.join()       
        
        if self._verbose:
            print(', time elapsed: ', round(time.time() - start_time, 3), 
                ' seconds', sep = '')
        
        return [r.get() for r in results]