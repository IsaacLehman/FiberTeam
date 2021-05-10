'''
    BY: Isaac Lehman
    An easy approach to multithreading in python.

    STEPS:
        1. Import
            from fiberTeam import FiberTeam
        2. Make some Fibers
            myFibers = FiberTeam(50)
        3. Run
            fiber_id = myFibers.add_fiber(function=make_pi, args=(arg1, arg2, ...))

            -or-

            @myFibers.Fiberize()
            def make_pi(thread_id, arg1, arg2, ...):
                ...

            make_pi(1,2,3...)
            make_pi(1,2,3...)
            ...
            make_pi(1,2,3...)
        4. Get result
            result = myFibers.join_fiber(fiber_id)

        def make_pi(thread_id, arg1, arg2, ...)




Lock()
'''

from threading import Thread, Lock
from dataclasses import dataclass
from functools import wraps


@dataclass
class FiberTeam:
    NUMBER_OF_THREADS: int
    verbose: bool = False
    RETURNS = []
    THREADS = []

    # ----------------------------------------
    # SETUP
    # ----------------------------------------
    def __post_init__(self):
        for i in range(self.NUMBER_OF_THREADS):
            self.THREADS.append(('FREE', None))  # initialise to not used
            self.RETURNS.append([])

    # ----------------------------------------
    # GETTERS
    # ----------------------------------------
    def get_num_free_fibers(self):
        count = 0
        for i in range(self.NUMBER_OF_THREADS):
            if self.THREADS[i][0] == 'FREE':
                count += 1
        return count  # none found

    def get_fibers_in_use(self):
        used_ids = []
        for i in range(self.NUMBER_OF_THREADS):
            if self.THREADS[i][0] == 'USED':
                used_ids.append(i)
        return used_ids  # none found

    def get_next_free_fiber(self):
        for i in range(self.NUMBER_OF_THREADS):
            if self.THREADS[i][0] == 'FREE':
                return i
        return None  # none found

    def get_fibers_status(self, thread_id):
        if thread_id > self.NUMBER_OF_THREADS:
            return None
        return self.THREADS[thread_id][0]

    # ----------------------------------------
    # THE THREAD FUNCTION
    # ----------------------------------------
    def thread_func(self, thread_num, func, args):
        try:
            result = func(thread_num, *args)
        except Exception as e:
            print("ERROR: Thread -> ", thread_num)
            print(e)
            result = None
        if self.verbose:
            print('Fiber - ', thread_num, ' - Done!')
        self.RETURNS[thread_num] = result
        return

    def Fiberized_ThreadFunc(self, thread_id, func, args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            print("ERROR: Thread -> ", thread_id)
            print(e)
            result = None
        if self.verbose:
            print('Fiber - ', thread_id, ' - Done!')
        self.RETURNS[thread_id] = result

    def Fiberized_ProcessesFunc(self, thread_id, func, args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            print("ERROR: Thread -> ", thread_id)
            print(e)
            result = None
        if self.verbose:
            print('Fiber - ', thread_id, ' - Done!')
        # self.RETURNS[thread_id] = result

    # ----------------------------------------
    # MAKING/JOINING MULTIPLE FIBERS
    # ----------------------------------------
    # args is a tuple
    def make_fibers(self, num_threads, function, args):
        # MAKE SURE THERE ARE ENOUGH THREADS
        if self.get_num_free_fibers() < num_threads:
            print('ERROR: Not enough free fibers.')
            return None

        # Create and start the Thread objects.
        for i in range(0, num_threads):
            thread_id = self.get_next_free_fiber()
            curThread = Thread(target=self.thread_func, args=(thread_id, function, args))
            self.THREADS[thread_id] = ('USED', curThread)
            self.RETURNS[thread_id] = None
            curThread.start()

    def join_fibers(self):
        results = []
        # Wait for all threads to end.
        for i in range(self.NUMBER_OF_THREADS):
            if self.THREADS[i][0] == 'USED':
                self.THREADS[i][1].join()
                self.THREADS[i] = ('FREE', None)
                results.append(self.RETURNS[i])
                self.RETURNS[i] = None

        return results

    # ----------------------------------------
    # MAKING/JOINING SINGLE FIBERS
    # ----------------------------------------
    # args is a tuple
    def add_fiber(self, function, args):
        # Create and start the Thread objects.
        thread_id = self.get_next_free_fiber()
        if thread_id is None:
            print('ERROR: Not enough free fibers.')
            return None
        curThread = Thread(target=self.thread_func, args=(thread_id, function, args))
        self.THREADS[thread_id] = ('USED', curThread)
        self.RETURNS[thread_id] = None
        curThread.start()
        return thread_id

    def join_fiber(self, thread_id):
        if self.THREADS[thread_id][0] == 'USED':
            self.THREADS[thread_id][1].join()
            self.THREADS[thread_id] = ('FREE', None)
            results = self.RETURNS[thread_id]
            self.RETURNS[thread_id] = None
            return results
        else:
            return None

    # ----------------------------------------
    # FIBERIZATION
    # myFibers = FiberTeam(50)
    # usage: @myFibers.Fiberize
    # ----------------------------------------
    def Fiberize(self, save_results=True):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                thread_id = self.get_next_free_fiber()

                if (save_results):
                    all_args = (thread_id, func, args)
                    curThread = Thread(target=self.Fiberized_ThreadFunc, args=all_args, kwargs=kwargs)
                else:
                    curThread = Thread(target=func, args=args, kwargs=kwargs)

                self.THREADS[thread_id] = ('USED', curThread)
                self.RETURNS[thread_id] = None

                curThread.start()
            return wrapper
        return decorator
