'''
The first problem is: Given a 2D matrix (or list of lists), count how many numbers are present between a given range
in each row. We will work on the list prepared below.

'''
import ctypes

import numpy as np
# import multiprocessing as mp
from multiprocessing import Pool, Array, Process, cpu_count, RawArray
import timer_wraper as tw


def howmany_within_range(row, minimum, maximum):
    """Returns how many numbers lie within `maximum` and `minimum` in a given `row`"""
    count = 0
    for n in row:
        if minimum <= n <= maximum:
            count = count + 1
    for _ in range(10000):
        count = count + 1
    return count


@tw.timeit
def sequential_apply(data, func):
    results = []
    for row in data:
        results.append(func(row, 4, 8))
    return results


@tw.timeit
def parallelize_pool_apply(data, func, cpus=cpu_count()):
    # Parallelizing using Pool.apply()

    # Step 1: Init multiprocessing.Pool()
    # pool = Pool(cpu_count())

    pool = Pool(cpus)
    # print(cpu_count())

    # shared_array = RawArray(ctypes.c_double, data.size)
    # shared_array_np = np.ndarray(data.shape, dtype=data.dtype, buffer=shared_array)
    # # Copy data to our shared array.
    # np.copyto(shared_array_np, data)

    # Step 2: `pool.apply` the `howmany_within_range()`
    # results = pool.starmap(howmany_within_range,[(row, 4, 8)) for row in data])

    results = pool.starmap(func, [(row, 4, 8) for row in data])

    # Step 3: Don't forget to close
    pool.close()

    return results


if __name__ == '__main__':
    # Prepare data
    np.random.RandomState(100)
    arr = np.random.randint(0, 10, size=[50, 500000])
    data = arr

    # Without parallelization
    results = sequential_apply(data, howmany_within_range)
    print(sum(results))

    # Parallelize using Pool.apply()

    for i in range(1, 50):
        results = parallelize_pool_apply(data, howmany_within_range, i)
        print(f"Number of workers: {i}")

    print(sum(results))
