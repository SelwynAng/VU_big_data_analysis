import multiprocessing as mp
import timer_wraper as tw

@tw.timeit
def worker():
    print('Worker started...')
    for i in range(1, 10000000):
        pass
    print('Worker finished...')
    
@tw.timeit
def sequential():
    worker()
    worker()
    worker()
    worker()
    
@tw.timeit
def parallel():
    p1 = mp.Process(target=worker)
    p2 = mp.Process(target=worker)
    p3 = mp.Process(target=worker)
    p4 = mp.Process(target=worker)

    p1.start()
    p2.start()
    p3.start()
    p4.start()
    
    p1.join()
    p2.join()
    p3.join()
    p4.join()

'''
Note that we enclosed the code to create and start the process inside the 
if __name__ == '__main__': block. 
This is necessary to prevent the newly created process from trying to start its own subprocesses, 
which can lead to unexpected behavior.
'''
if __name__ == '__main__':
    # p = multiprocessing.Process(target=worker)
    # p.start()
    # print("Main process continues to run...")
    sequential()
    parallel()
    # p.join()
    # print("Main process waits for the worker process to finish...")


