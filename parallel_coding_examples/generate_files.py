'''
We genarating multiple files filled with random data.
'''

import os
import random
import string
import timer_wraper as tw
import threading
import multiprocessing


# def generate_random_string(length=10):
#     random_space = string.ascii_letters + ' ' + string.digits + string.punctuation
#     return ''.join(random.choices(random_space, k=length))


class RandomString:
    _random_string=None

    @classmethod
    def generate(cls, length=10):
        if cls._random_string is None:
            random_space = string.ascii_letters + ' ' + string.digits + string.punctuation
            cls._random_string = ''.join(random.choices(random_space, k=length))
            return cls._random_string
        return cls._random_string

@tw.timeit
def generate_random_files(directory, n_files=100, file_size=1024):
    if not os.path.exists(directory):
        os.makedirs(directory)

    random_string = RandomString.generate(file_size)
    for i in range(n_files):
        file_path = os.path.join(directory, f'file_{i}.txt')
        with open(file_path, 'w') as file:
            file.write(random_string)


def write_a_file(file_path, file_size):
    random_string = RandomString.generate(file_size)
    with open(file_path, 'w') as file:
        file.write(random_string)


@tw.timeit
def generate_random_files_parallel(directory, n_files=100, file_size=1024):
    if not os.path.exists(directory):
        os.makedirs(directory)

    the_threads = []
    for i in range(n_files):
        file_path = os.path.join(directory, f'file_{i}.txt')
        thread = threading.Thread(target=write_a_file, args=(file_path, file_size))
        thread.start()
        the_threads.append(thread)
    print('the_threads')

    for thread in the_threads:
        thread.join()

    print('end_threads')


@tw.timeit
def generate_random_files_parallel_proc(directory, n_files=100, file_size=1024):
    if not os.path.exists(directory):
        os.makedirs(directory)

    pool = multiprocessing.Pool(multiprocessing.cpu_count()-2)
    data = [(os.path.join(directory, f'file_{i}.txt'), file_size) for i in range(n_files)]
    pool.starmap(write_a_file, data)
    pool.close()
    pool.join()


if __name__ == '__main__':

    n_files = 1000
    file_size = 1024000

    #Generate 100 files in the 'random_files' directory sequentially
    print('Sequential:')
    generate_random_files('random_files', n_files=n_files, file_size=file_size)

    print('\nParallel:')
    # Generate 100 files in the 'random_files' directory in parallel
    generate_random_files_parallel('random_files', n_files=n_files, file_size=file_size)

    print('\nParallel with processes:')
    # Generate 100 files in the 'random_files' directory in parallel
    generate_random_files_parallel_proc('random_files', n_files=n_files, file_size=file_size)




