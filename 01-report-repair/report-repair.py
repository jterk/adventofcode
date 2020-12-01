#!/usr/bin/env python
#
# Solution for https://adventofcode.com/2020/day/1
#
# Read `input`, find the two numbers that sum to `2020, and output their product.
#
# Expects `input` to contain integers, one per line.
import functools
import itertools
import operator

numbers = []

with open('input', 'r') as f:
    for line in f:
        numbers.append(int(line))

# Change `repeat` to compute pairs, triples, etc.
for t in itertools.product(numbers, repeat=3):
    if sum(t) == 2020:
        print('{} sum to 2020; their product is {}'.format(t, functools.reduce(operator.mul, t)))
        exit()
