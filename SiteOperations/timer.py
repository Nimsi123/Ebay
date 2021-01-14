import time
import functools

globalTimeTotal = 0
globalTimeCounter = 0

def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        global globalTimeTotal, globalTimeCounter
        tic = time.perf_counter()
        value = func(*args, **kwargs)
        toc = time.perf_counter()
        elapsed_time = toc - tic

        globalTimeTotal += elapsed_time
        globalTimeCounter += 1
        print("average elapsed time: ", globalTimeTotal/globalTimeCounter)
        #print(f"Elapsed time: {elapsed_time:0.8f} seconds")
        return value
    return wrapper_timer