from numba import jit, cuda
import numpy as np
# to measure exec time
from timeit import default_timer as timer

# normal function to run on cpu


def func(a):
    for i in range(10000000):
        a[i] += 1

# function optimized to run on gpu


@jit(target_backend='cuda')
def func2(a):
    for i in range(10000000):
        a[i] += 1


if __name__ == "__main__":
    n = 10000000
    a = np.ones(n, dtype=np.float64)
    iteration = 100
    cpu_times = []
    gpu_times = []

    for _ in range(iteration):
        start = timer()
        func(a)
        cpu_times.append(timer() - start)

    for _ in range(iteration):
        start = timer()
        func2(a)
        gpu_times.append(timer() - start)

    avg_cpu_time = sum(cpu_times)/100
    avg_gpu_time = sum(gpu_times)/100

    print("Average CPU time:", avg_cpu_time)
    print("Average GPU time:", avg_gpu_time)
