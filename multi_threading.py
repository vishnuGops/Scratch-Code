import time
import threading


def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


def main():
    start_time = time.time()
    print("Calculating Fibonacci numbers using multithreading...")
    print("Start time: ", start_time)
    num_threads = 10  # You can adjust this to test different levels of concurrency

    # The number of Fibonacci numbers to calculate
    num_fibonacci = 10

    # Split the task into equal chunks for each thread
    chunk_size = num_fibonacci // num_threads
    ranges = [(i * chunk_size + 1, (i + 1) * chunk_size)
              for i in range(num_threads)]

    # Create and start the threads
    threads = []
    for i in range(num_threads):
        start, end = ranges[i]
        thread = threading.Thread(
            target=lambda: [fibonacci(x) for x in range(start, end + 1)])
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    end_time = time.time()
    print("End time: ", end_time)
    elapsed_time = end_time - start_time
    print("Total time taken: ", elapsed_time)


if __name__ == "__main__":
    main()
