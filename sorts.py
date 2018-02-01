#!/usr/bin/python3
# Copyright (c) 2018 Bart Massey
# This work is licensed under the "MIT License". Please see
# the file LICENSE in this distribution for license terms.

from random import randrange
import sys
import time

# Some sorts: Quicksort, Heapsort

# Constants for array testing.
arrays_count = 10
arrays_len = 1000
arrays_range = 500

# Array a must have at least 1 element.
# Rearrange a so that all elements <= a[m]
# are before position m, the "pivot" position.
# Uses middle element as pivot unless m3
# is true, in which case uses median of
# first, middle and last element.
def partition(a, start, end, m3=True):
    # No pivot is possible in 0-length arrays.
    n = end - start
    assert n > 0
    # For length 1 arrays, just do the obvious.
    if n == 1:
        return 0

    # Pick a pivot and swap it to the start position.
    mid_index = start + (end - start) // 2
    if m3:
        # Hairy unrolled median calculation.
        low_index = start
        high_index = end - 1
        if a[low_index] > a[high_index]:
            low_index, high_index = high_index, low_index
        if a[mid_index] < a[low_index]:
            mid_index = low_index
        elif a[mid_index] > a[high_index]:
            mid_index = high_index
    if mid_index != start:
        a[start], a[mid_index] = a[mid_index], a[start]

    # Partition the array.
    left = start + 1
    right = end - 1
    while True:
        while left < right and a[left] <= a[start]:
            left += 1
        while right > left and a[right] > a[start]:
            right -= 1
        if left >= right:
            if a[left] > a[start]:
                left -= 1
            a[start], a[left] = a[left], a[start]
            return left
        a[left], a[right] = a[right], a[left]
        left += 1
        right -= 1

# Generate random arrays and call check function on them.
def test_on_arrays(check):
    for _ in range(arrays_count):
        n = randrange(1, arrays_len)
        a = [randrange(arrays_range) for _ in range(n) ]
        check(a)

# Check partitioning of array a.
def check_partition(a, m3):
    m = partition(a, 0, len(a), m3)
    for i in range(m):
        if a[i] > a[m]:
            print("failed low", m, a)
            exit(1)
    for i in range(m + 1, len(a)):
        if a[i] <= a[m]:
            print("failed high", m, a)
            exit(1)

# Sort an array a using quicksort.
def quicksort(a, start=0, end=None, m3=True):
    if end == None:
        end = len(a)
    if end - start <= 1:
        return
    m = partition(a, start, end, m3)
    quicksort(a, start, m, m3)
    quicksort(a, m + 1, end, m3)

# Check sort of array a.
def check_sort(sortname, sort):
    def check(a):
        expected = sorted(list(a))
        sort(a)
        if a != expected:
            print(sortname, "mismatch", a, expected)
            exit(1)
    return check
    
# Downheap maxheap a starting at position i.
def downheap(a, start=0, end=None):
    n = len(a)
    if end == None:
        end = n
    while True:
        left = 2 * start + 1
        right = 2 * start + 2
        nexti = start
        if left < end and a[left] > a[nexti]:
            nexti = left
        if right < end and a[right] > a[nexti]:
            nexti = right
        if nexti == start:
            return
        a[start], a[nexti] = a[nexti], a[start]
        start = nexti

# Make a into a heap.
def heapify(a):
    n = len(a)
    for i in reversed(range((n-2) // 2 + 1)):
        downheap(a, start=i)

# Check heapify of array a.
def check_heapify(a):
    n = len(a)
    heapify(a)
    for i in range(n):
        left = 2 * i + 1
        if left < n:
            assert a[i] >= a[left]
        right = 2 * i + 2
        if right < n:
            assert a[i] >= a[right]

# Heapsort
def heapsort(a):
    n = len(a)
    heapify(a)
    for dest in reversed(range(1, n)):
        a[dest], a[0] = a[0], a[dest]
        downheap(a, end=dest)

test_on_arrays(lambda a: check_partition(a, m3=True))
test_on_arrays(lambda a: check_partition(a, m3=False))
test_on_arrays(check_sort("quicksort", lambda a: quicksort(a, m3=True)))
test_on_arrays(check_sort("quicksort", lambda a: quicksort(a, m3=False)))
test_on_arrays(check_heapify)
test_on_arrays(check_sort("heapsort", heapsort))

# Benchmark a given sort by passing arrays of doubling size
# until runtime exceeds 5s. Write this info into logfile
# for future graphing.
def bench(sortname, sort):

    # Get wall-clock time of run of sort on a.
    def runtime(a):
        start_time = time.perf_counter()
        sort(a)
        end_time = time.perf_counter()
        return end_time - start_time

    # Produce the trace.
    print(sortname + ":", flush=True, end="")
    with open(sortname + ".plot", "w") as log:
        n = 1
        t = runtime([0])
        while t < 5.0:
            n *= 2
            a = [randrange(n//2) for _ in range(n) ]
            print("", n, flush=True, end="")
            t = runtime(a)
            print(n, t, file=log)
        print()

bench("heapsort", heapsort)
bench("quicksort-m3", lambda a: quicksort(a, m3=True))
bench("quicksort-m", lambda a: quicksort(a, m3=False))
