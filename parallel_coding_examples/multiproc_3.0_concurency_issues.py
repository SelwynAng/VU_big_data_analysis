import multiprocessing
import time


# Function to increment a shared counter
def increment_counter(shared_counter):
    # initial value of shared_counter is 0
    # cycle runs 1000 times
    # each cycle takes 0.00001 seconds
    # so, the final value of shared_counter should be 1000
    for _ in range(1000):
        time.sleep(0.00001)  # simulate some work
        shared_counter.value += 1


def demonstrate_concurrency_issue():
    # Shared counter variable
    shared_counter = multiprocessing.Value('i', 0)

    # Creating multiple processes
    # processes = [multiprocessing.Process(target=increment_counter, args=(shared_counter,)) for _ in range(4)]

    processes = []
    for _ in range(4):
        process = multiprocessing.Process(target=increment_counter, args=(shared_counter,))
        processes.append(process)


    # Start the processes
    for p in processes:
        p.start()

    # Wait for all processes to complete
    for p in processes:
        p.join()

    # Print the final value of the shared counter
    print(f"Final value of the counter: {shared_counter.value}")


if __name__ == "__main__":
    demonstrate_concurrency_issue()
