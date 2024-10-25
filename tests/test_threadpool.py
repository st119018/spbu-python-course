import pytest
import time
import threading
from math import ceil
from project.threadpool.threadpool import ThreadPool


def some_func(sec: int):
    # simulate some work
    # sleep for several seconds
    time.sleep(sec)


def test_threadpool_enqueue():
    pool = ThreadPool(3)
    pool.enqueue(some_func, 2)

    # ensure task is added
    assert len(pool.tasks) == 1

    pool.dispose()


def test_threadpool_dispose():
    pool = ThreadPool(3)

    pool.enqueue(some_func, 1)
    pool.dispose()

    assert len(pool.tasks) == 0

    # new tasks can't be added
    # after dispose() is called
    pool.enqueue(some_func, 3)
    assert len(pool.tasks) == 0


def test_threadpool_number_of_threads():
    old_count = threading.active_count()
    pool = ThreadPool(4)
    new_count = threading.active_count()
    pool.dispose()

    # ensure that 4 threads were created in threadpool
    assert new_count - old_count == 4
    # ensure threads in threadpool are joined
    assert old_count == threading.active_count()


def test_threadpool_invalid_number_of_threads():
    with pytest.raises(ValueError):
        ThreadPool(-1)


def test_threadpool():
    count = [0]
    lock = threading.Lock()

    def add():
        with lock:
            count[0] += 1

    pool = ThreadPool(2)
    for _ in range(11):
        pool.enqueue(add)
    pool.dispose()

    # ensure that all 11 tasks are done
    assert count[0] == 11


def test_threadpool_time():
    pool = ThreadPool(3)
    start = time.time()
    for _ in range(10):
        pool.enqueue(some_func, 3)
    pool.dispose()
    end = time.time()

    assert end - start == pytest.approx(ceil(10 / 3) * 3, 2)
