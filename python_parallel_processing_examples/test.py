import numpy as np
import multiprocessing as mp

from time import time

def howmany_within_range(row, minimum, maximum):
    count = 0
    for n in row:
        if minimum <= n <= maximum:
            count = count + 1
    return count

def howmany_within_rangeonly(row, minimum=4, maximum=8):
    count = 0
    for n in row:
        if minimum <= n <= maximum:
            count = count + 1
    return count

def howmany_within_range2(i, row, minimum, maximum):
    count = 0
    for n in row:
        if minimum <= n <= maximum:
            count = count + 1
    return (i, count)

def collect_result(result):
    global results
    results.append(result)


if __name__ == '__main__':
    np.random.RandomState(100)
    arr = np.random.randint(0, 10, size=[20000, 5])
    data = arr.tolist()
    data[:5]

    # Serial execution
    results = []
    start_time_serial = time()
    
    for row in data:
        results.append(howmany_within_range(row, minimum=4, maximum=8))
    
    end_time_serial = time()
    
    print("Serial execution time:", end_time_serial - start_time_serial)
    print(results[:10])

    # Parallel execution with Pool's apply
    results = []
    start_time_apply = time()
    
    pool = mp.Pool(mp.cpu_count())
    results = [pool.apply(howmany_within_range, args=(row, 4, 8)) for row in data]
    pool.close()
    
    end_time_apply = time()
    print("Parallel (apply) execution time:", end_time_apply - start_time_apply)
    print(results[:10])
    
    # Parellel execution with Pool's map
    results = []
    start_time_map = time()
    
    pool = mp.Pool(mp.cpu_count())
    results = pool.map(howmany_within_rangeonly, [row for row in data])
    pool.close()
    
    end_time_map = time()
    
    print("Parallel (map) execution time:", end_time_map - start_time_map)
    print(results[:10])
    
    # Parallel execution with Pool's starmap
    results = []
    start_time_starmap = time()
    
    pool = mp.Pool(mp.cpu_count())
    results = pool.starmap(howmany_within_range, [(row, 4, 8) for row in data])
    pool.close()
    
    end_time_starmap = time()
    print("Parallel (starmap) execution time:", end_time_starmap - start_time_starmap)
    print(results[:10])
    
    # Parallel execution with Pool's apply_async
    start_time_apply_async = time()
    results = []
    pool = mp.Pool(mp.cpu_count())
    for i, row in enumerate(data):
        pool.apply_async(howmany_within_range2, args=(i, row, 4, 8),
        callback=collect_result)
    pool.close()
    pool.join()

    results.sort(key=lambda x: x[0])
    results_final = [r for i, r in results]
    end_time_apply_async = time()
    print("Parallel (apply_async) execution time:", end_time_apply_async - start_time_apply_async)
    print(results_final[:10])