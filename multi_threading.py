import time
import threading


def fibonacci(n):
    # Only print for the top-level call in each thread
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


def thread_task(start, end, thread_id):
    print(
        f"Thread {thread_id} started: calculating Fibonacci numbers from {start} to {end}")
    results = []
    for x in range(start, end + 1):
        result = fibonacci(x)
        results.append((x, result))
    print(f"Thread {thread_id} finished. Results: {results}")


def main():
    start_time = time.time()
    print("Calculating Fibonacci numbers using multithreading...")
    num_threads = 10
    num_fibonacci = 20

    chunk_size = num_fibonacci // num_threads
    ranges = [(i * chunk_size + 1, (i + 1) * chunk_size)
              for i in range(num_threads)]

    print(f"Number of threads: {num_threads}")
    print(f"Number of Fibonacci numbers: {num_fibonacci}")

    threads = []
    for i in range(num_threads):
        start, end = ranges[i]
        thread = threading.Thread(
            target=thread_task, args=(start, end, i + 1))
        threads.append(thread)
        print(f"Starting Thread {i + 1} for range {start}-{end}")
        thread.start()

    for i, thread in enumerate(threads):
        thread.join()
        print(f"Thread {i + 1} has completed.")

    end_time = time.time()
    print("Total time taken: ", end_time - start_time)


if __name__ == "__main__":
    main()
