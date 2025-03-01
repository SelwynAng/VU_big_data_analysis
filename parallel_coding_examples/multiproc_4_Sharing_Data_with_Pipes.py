import multiprocessing


def worker(conn):
    while True:             # Loop until the parent process sends a stop message
        msg = conn.recv()   # Receive a message from the parent process
        if msg == 'stop':   # Check for the stop
            break
        res = msg * 2       # Process the message
        conn.send(res)      # Send the result back to the parent process


if __name__ == '__main__':
    parent_conn, child_conn = multiprocessing.Pipe()
    p = multiprocessing.Process(target=worker, args=(child_conn,))
    p.start()

    # Send some messages to the child process
    parent_conn.send(10)        # The child process will receive these messages
    parent_conn.send(20)        # The child process will receive these messages
    parent_conn.send(30)        # The child process will receive these messages
    parent_conn.send('stop')    # Send the stop message
    p.join()                    # Wait for the child process to finish

    # Receive the results from the child process
    while parent_conn.poll():
        result = parent_conn.recv()
        print(result)
