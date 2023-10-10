import time


def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def find_primes_in_range(start, end):
    primes = []
    for num in range(start, end + 1):
        if is_prime(num):
            primes.append(num)
    return primes


if __name__ == "__main__":
    start_range = 1
    end_range = 1000000  # Adjust the range as needed for more or less computation

    print(f"Finding prime numbers between {start_range} and {end_range}...")

    start_time = time.time()
    primes = find_primes_in_range(start_range, end_range)
    end_time = time.time()

    elapsed_time = end_time - start_time

    print(f"Found {len(primes)} prime numbers.")
    print(f"Time taken: {elapsed_time} seconds")
