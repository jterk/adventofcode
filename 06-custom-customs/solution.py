#!/usr/bin/env python
#
# Solution to https://adventofcode.com/2020/day/6
#
from functools import reduce
from operator import add

def sum_questions1(input):
    return reduce(add, [len(set(group.replace('\n', ''))) for group in input.split('\n\n')])

def sum_questions2(input):
    groups = [group for group in input.split('\n\n')]
    group_answers = [set(a) for a in [l.split('\n') for l in groups]]
    print(group_answers)
    group_unanimous  = [reduce(lambda x, y : set(x).intersection(set(y)), ga) for ga in group_answers]
    # print(group_unanimous)
    return reduce(add, [len(gu) for gu in group_unanimous])

SAMPLE ='''abc

a
b
c

ab
ac

a
a
a
a

b'''

# Part 1
sample_sum = sum_questions1(SAMPLE)
assert sample_sum == 11

# Note: Manually removed a trailing newline from the input to get the correct answer for part 2
input = ''
with open('input', 'r') as f:
    input = f.read()

problem_sum = sum_questions1(input)
print('Sum: {}'.format(problem_sum))

# Part 2
sample_sum2 = sum_questions2(SAMPLE)
assert sample_sum2 == 6

problem_sum2 = sum_questions2(input)
print('Sum2: {}'.format(problem_sum2))
