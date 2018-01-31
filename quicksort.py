#!/usr/bin/python3
# Copyright (c) 2018 Bart Massey

from random import randrange

# Quicksort

# Rearrange a so that all elements <= a[0]
# are before position m. Return m.
def partition(a):
    print("*input", a)
    n = len(a)
    left = 1
    right = n - 1
    i = 0
    while True:
        i += 1
        print("step", i, left, right)
        while left < right and a[left] <= a[0]:
            left += 1
        print("  left", left, right)
        while right > left and a[right] > a[0]:
            right -= 1
        print("  right", left, right)
        if left >= right:
            if left < n and a[left] <= a[0]:
                left += 1
            print("* return", left, right)
            return left
        a[left], a[right] = a[right], a[left]
        left += 1
        right -= 1

# Generate random arrays, partition them
# and check
def test_partition():
    for _ in range(100):
        n = randrange(1, 10)
        a = [randrange(500) for _ in range(n) ]
        m = partition(a)
        for i in range(m):
            if a[i] > a[0]:
                print("failed low", m, a)
                exit(1)
        for i in range(m, n):
            if a[i] <= a[0]:
                print("failed high", m, a)
                exit(1)

test_partition()
