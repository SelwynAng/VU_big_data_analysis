import multiprocessing
import time

# Function to increment a shared counter with a lock for synchronization
def increment_counter(shared_counter, lock):
    for _ in range(1000):
        time.sleep(0.0001)  # simulate some work
        with lock:
            shared_counter.value += 1

def demonstrate_no_concurrency_issue():
    # Shared counter variable
    shared_counter = multiprocessing.Value('i', 0)

    # Lock for synchronizing access to the shared counter
    lock = multiprocessing.Lock()

    # Creating multiple processes
    processes = [multiprocessing.Process(target=increment_counter, args=(shared_counter, lock)) for _ in range(4)]

    # Start the processes
    for p in processes:
        p.start()

    # Wait for all processes to complete
    for p in processes:
        p.join()

    # Print the final value of the shared counter
    print(f"Final value of the counter: {shared_counter.value}")


if __name__ == "__main__":
    demonstrate_no_concurrency_issue()
