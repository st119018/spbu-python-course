"""This module provides access to thread pool.

Classes
-------
ThreadPool
"""
import threading
from typing import Callable, List, Tuple, Any


class ThreadPool:
    """Class implements thread pool.

    Tasks given to thread pool are executed in parallel.

    Attributes
    ----------
    num_thread : int
        Number of threads to be created
    threads : List[threading.Thread]
        List of threads
    tasks : List[Tuple[Callable, Tuple, dict]]
        List of functions with arguments to call in thread
    is_finished : bool
        Flag that is raised if tasks are no longer accepted
    event : threading.Event
        Event to communicate between threads
    lock : threading.Lock
        Lock for tasks

    Methods
    -------
    _worker()
        Execute tasks
    enqueue(task, *args, **kwargs)
        Add new task
    dispose()
        Shut down thread pool
    """

    def __init__(self, num_thread: int):
        """Set attributes and starts given number of threads.

        Parameters
        ----------
        num_thread : int
            Number of threads to create in pool

        Raises
        ------
        ValueError
            If num_thread isn't positive
        """

        if num_thread <= 0:
            raise ValueError("Inappropriate number of threads")

        self.max_number = num_thread
        self.threads: List[threading.Thread] = []
        self.tasks: List[Tuple[Callable, Tuple, dict]] = []
        self.is_finished = False
        self.event = threading.Event()
        self.lock = threading.Lock()

        for _ in range(self.max_number):
            thread = threading.Thread(target=self._worker)
            thread.start()
            self.threads.append(thread)

    def _worker(self):
        """Take first added task from tasks.
        Taken task is deleted from tasks.

        Execute task in separate thread.
        """
        while not self.is_finished:
            # wait until task is added or dispose() is called
            self.event.wait()
            self.event.clear()

            # take first task from tasks
            with self.lock:
                if len(self.tasks) > 0:
                    first = self.tasks.pop(0)
                else:
                    first = ()

            if len(first) != 0:
                # execute task
                task, args, kwargs = first
                task(*args, **kwargs)

        # executing tasks without waiting
        # after dispose() is called
        # if there are any left
        num = 1
        while num > 0:
            is_left = False
            with self.lock:
                num = len(self.tasks)
                if num > 0:
                    is_left = True
                    task, args, kwargs = self.tasks.pop(0)

            # wake up threads if there are any left waiting
            self.event.set()

            if is_left:
                task(*args, **kwargs)

    def enqueue(self, task: Callable, *args: Any, **kwargs: Any):
        """Add new task to be executed if dispose() isn't called.

        Parameters
        ----------
        task : Callable
            Function to execute in thread
        args : Any
            Positional arguments of task function
        kwargs : Any
            Keyword arguments of task function
        """
        if not self.is_finished:
            with self.lock:
                self.tasks.append((task, args, kwargs))

            self.event.set()

    def dispose(self):
        """Finish work of thread pool
        and wait until all threads are joined.
        """
        self.event.set()
        self.is_finished = True

        for thread in self.threads:
            thread.join()
