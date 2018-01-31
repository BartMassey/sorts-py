#!/usr/bin/python3
# Copyright (c) 2018 Bart Massey

from random import randrange

# Quicksort

# Array a must have at least 1 element.
# Rearrange a so that all elements <= a[0]
# are before position m with a[0] at position m - 1.
# Return m.
def partition(a, start, end):
    assert end - start > 0
    left = start + 1
    right = end - 1
    while True:
        while left < right and a[left] <= a[start]:
            left += 1
        while right > left and a[right] > a[start]:
            right -= 1
        if left >= right:
            if left < end and a[left] <= a[start]:
                left += 1
            a[start], a[left-1] = a[left-1], a[start]
            return left
        a[left], a[right] = a[right], a[left]
        left += 1
        right -= 1

# Generate random arrays and call check function on them.
def test_on_arrays(check):
    for _ in range(1000):
        n = randrange(1, 1000)
        a = [randrange(500) for _ in range(n) ]
        check(a)

# Check partitioning of array a.
def check_partition(a):
    m = partition(a, 0, len(a))
    for i in range(m):
        if a[i] > a[m-1]:
            print("failed low", m, a)
            exit(1)
    for i in range(m, len(a)):
        if a[i] <= a[m-1]:
            print("failed high", m, a)
            exit(1)

# Sort an array a using quicksort.
def quicksort(a, start=0, end=None):
    if end == None:
        end = len(a)
    if end - start <= 1:
        return
    m = partition(a, start, end)
    quicksort(a, start, m-1)
    quicksort(a, m, end)

# Check quicksort of array a.
def check_quicksort(a):
    expected = sorted(list(a))
    quicksort(a)
    if a != expected:
        print("quicksort mismatch", a, expected)
        exit(1)
    
test_on_arrays(check_partition)
test_on_arrays(check_quicksort)
