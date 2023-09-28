import random
import time
import pandas as pd

# Implementation of sorting algorithms


def bubble_sort(arr):
    comparisons = 0
    swaps = 0
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            comparisons += 1
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swaps += 1
    return comparisons, swaps


def selection_sort(arr):
    comparisons = 0
    swaps = 0
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            comparisons += 1
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        swaps += 1
    return comparisons, swaps


def insertion_sort(arr):
    comparisons = 0
    swaps = 0
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            comparisons += 1
            arr[j + 1] = arr[j]
            swaps += 1
            j -= 1
        arr[j + 1] = key
    return comparisons, swaps


def merge_sort(arr):
    comparisons = 0
    swaps = 0
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        comparisons_left, swaps_left = merge_sort(left_half)
        comparisons_right, swaps_right = merge_sort(right_half)

        comparisons += comparisons_left + comparisons_right
        swaps += swaps_left + swaps_right

        i = j = k = 0

        while i < len(left_half) and j < len(right_half):
            comparisons += 1
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

    return comparisons, swaps


def quick_sort(arr):
    def partition(low, high):
        nonlocal comparisons, swaps
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            comparisons += 1
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                swaps += 1
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        swaps += 1
        return i + 1

    def quick_sort_helper(low, high):
        if low < high:
            pi = partition(low, high)
            quick_sort_helper(low, pi - 1)
            quick_sort_helper(pi + 1, high)

    comparisons = 0
    swaps = 0
    quick_sort_helper(0, len(arr) - 1)
    return comparisons, swaps


def heap_sort(arr):
    def heapify(n, i):
        nonlocal comparisons, swaps
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and arr[i] < arr[left]:
            comparisons += 1
            largest = left

        if right < n and arr[largest] < arr[right]:
            comparisons += 1
            largest = right

        if largest != i:
            swaps += 1
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(n, largest)

    def build_heap():
        n = len(arr)
        for i in range(n // 2 - 1, -1, -1):
            heapify(n, i)

    comparisons = 0
    swaps = 0
    build_heap()
    for i in range(len(arr) - 1, 0, -1):
        swaps += 1
        arr[i], arr[0] = arr[0], arr[i]
        heapify(i, 0)
    return comparisons, swaps


def radix_sort(arr):
    def counting_sort(arr, exp):
        nonlocal comparisons, swaps
        n = len(arr)
        output = [0] * n
        count = [0] * 10

        for i in range(n):
            index = (arr[i] // exp) % 10
            count[index] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        i = n - 1
        while i >= 0:
            index = (arr[i] // exp) % 10
            output[count[index] - 1] = arr[i]
            count[index] -= 1
            i -= 1

        for i in range(n):
            swaps += 1
            arr[i] = output[i]

    def radix_sort_helper():
        max_num = max(arr)
        exp = 1
        while max_num // exp > 0:
            counting_sort(arr, exp)
            exp *= 10

    comparisons = 0
    swaps = 0
    radix_sort_helper()
    return comparisons, swaps


def counting_sort(arr):
    comparisons = 0
    swaps = 0
    max_num = max(arr)
    min_num = min(arr)
    range_of_elements = max_num - min_num + 1
    count_arr = [0] * range_of_elements
    output_arr = [0] * len(arr)

    for i in range(len(arr)):
        comparisons += 1
        count_arr[arr[i] - min_num] += 1

    for i in range(1, len(count_arr)):
        count_arr[i] += count_arr[i - 1]

    for i in range(len(arr) - 1, -1, -1):
        swaps += 1
        output_arr[count_arr[arr[i] - min_num] - 1] = arr[i]
        count_arr[arr[i] - min_num] -= 1

    for i in range(len(arr)):
        arr[i] = output_arr[i]

    return comparisons, swaps


# def bucket_sort(arr):
#     def insertion_sort_bucket(bucket):
#         for i in range(1, len(bucket)):
#             key = bucket[i]
#             j = i - 1
#             while j >= 0 and key < bucket[j]:
#                 bucket[j + 1] = bucket[j]
#                 j -= 1
#             bucket[j + 1] = key

#     comparisons = 0
#     swaps = 0
#     n = len(arr)
#     num_buckets = int(n ** 0.5)
#     max_value = max(arr)
#     min_value = min(arr)
#     bucket_range = (max_value - min_value) / num_buckets

#     buckets = [[] for _ in range(num_buckets)]

#     for num in arr:
#         index = int((num - min_value) / bucket_range)
#         buckets[index].append(num)

#     for i in range(num_buckets):
#         insertion_sort_bucket(buckets[i])

#     k = 0
#     for i in range(num_buckets):
#         for j in range(len(buckets[i])):
#             arr[k] = buckets[i][j]
#             k += 1

#     return comparisons, swaps


def shell_sort(arr):
    comparisons = 0
    swaps = 0
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                comparisons += 1
                arr[j] = arr[j - gap]
                swaps += 1
                j -= gap
            arr[j] = temp
        gap //= 2
    return comparisons, swaps


def tim_sort(arr):
    comparisons = 0
    swaps = 0
    n = len(arr)
    min_run = 32

    for start in range(0, n, min_run):
        end = min(start + min_run - 1, n - 1)
        insertion_sort(arr, start, end)

    size = min_run
    while size < n:
        for start in range(0, n, size * 2):
            mid = min(n - 1, start + size - 1)
            end = min(n - 1, mid + size)
            merge(arr, start, mid, end)

        size *= 2

    return comparisons, swaps


def cocktail_shaker_sort(arr):
    comparisons = 0
    swaps = 0
    n = len(arr)
    swapped = True
    start = 0
    end = n - 1

    while swapped:
        swapped = False

        for i in range(start, end):
            comparisons += 1
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swaps += 1
                swapped = True

        if not swapped:
            break

        swapped = False
        end -= 1

        for i in range(end - 1, start - 1, -1):
            comparisons += 1
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swaps += 1
                swapped = True

        start += 1

    return comparisons, swaps


def comb_sort(arr):
    comparisons = 0
    swaps = 0
    n = len(arr)
    gap = n
    shrink = 1.3
    sorted = False

    while not sorted:
        gap = int(gap / shrink)
        if gap > 1:
            sorted = False
        else:
            gap = 1
            sorted = True

        i = 0
        while i + gap < n:
            comparisons += 1
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                swaps += 1
                sorted = False
            i += 1

    return comparisons, swaps


def gnome_sort(arr):
    comparisons = 0
    swaps = 0
    n = len(arr)
    index = 0

    while index < n:
        if index == 0:
            index += 1
        comparisons += 1
        if arr[index] >= arr[index - 1]:
            index += 1
        else:
            arr[index], arr[index - 1] = arr[index - 1], arr[index]
            swaps += 1
            index -= 1

    return comparisons, swaps


def pancake_sort(arr):
    def flip(sub_list, k):
        i = 0
        while i < k:
            sub_list[i], sub_list[k] = sub_list[k], sub_list[i]
            i += 1
            k -= 1

    comparisons = 0
    swaps = 0
    n = len(arr)

    for curr_size in range(n, 1, -1):
        max_idx = arr.index(max(arr[:curr_size]))
        if max_idx != curr_size - 1:
            if max_idx != 0:
                flip(arr, max_idx)
                swaps += 1
            flip(arr, curr_size - 1)
            swaps += 1

    return comparisons, swaps


def bogo_sort(arr):
    def is_sorted(arr):
        for i in range(1, len(arr)):
            if arr[i] < arr[i - 1]:
                return False
        return True

    comparisons = 0
    swaps = 0

    while not is_sorted(arr):
        random.shuffle(arr)
        swaps += 1

    return comparisons, swaps


# Generating random list of 2048 numbers
numbers = [random.randint(1, 10000) for _ in range(2048)]

# Sorting algorithms to test
sorting_algorithms = [
    ("Bubble Sort", bubble_sort),
    ("Selection Sort", selection_sort),
    ("Insertion Sort", insertion_sort),
    ("Merge Sort", merge_sort),
    ("Quick Sort", quick_sort),
    ("Heap Sort", heap_sort),
    ("Radix Sort", radix_sort),
    ("Counting Sort", counting_sort),
    # ("Bucket Sort", bucket_sort),
    ("Shell Sort", shell_sort),
    ("Tim Sort", tim_sort),
    ("Cocktail Shaker Sort", cocktail_shaker_sort),
    ("Comb Sort", comb_sort),
    ("Gnome Sort", gnome_sort),
    ("Pancake Sort", pancake_sort),
    ("Bogo Sort", bogo_sort)
]

results = []

for algorithm_name, algorithm_func in sorting_algorithms:
    # Make a copy of the original list to ensure fairness in comparisons
    arr = numbers.copy()

    start_time = time.time()
    comparisons, swaps = algorithm_func(arr)
    end_time = time.time()

    elapsed_time = end_time - start_time

    results.append({
        "Algorithm": algorithm_name,
        "Comparisons": comparisons,
        "Swaps": swaps,
        "Time": elapsed_time
    })

# Saving results to a CSV file
results_df = pd.DataFrame(results)
results_df.to_csv("sorting_results.csv", index=False)

print("Sorting results saved to sorting_results.csv")
