import multiprocessing


def producer(queue):
    for i in range(10):
        queue.put(i)
    queue.put(None)


def consumer(queue):
    while True:
        item = queue.get()
        if item is None:
            break
        print(item)


if __name__ == '__main__':
    q = multiprocessing.Queue()
    p1 = multiprocessing.Process(target=producer, args=(q,))
    p2 = multiprocessing.Process(target=consumer, args=(q,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

# The Queue class is a thread and process safe way to share data between processes.
