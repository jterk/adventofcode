#!/usr/bin/env python
#
# Solution to https://adventofcode.com/2020/day/9
#
from collections import deque
from itertools import product

SAMPLE = '''35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576'''

def find_violation(input, buffer_len):
    buf = deque()

    for ln in input.split():
        if len(buf) == buffer_len:
            valid = any([int(ln) == a + b for a, b in product(buf, repeat=2)])

            if not valid:
                print('{} is not the sum of previous inputs'.format(ln))
                return int(ln)

            buf.popleft()

        buf.append(int(ln))

def find_parts(input, invalid):
    numbers = [int(ln) for ln in input.split()]

    for i, v in enumerate(numbers):
        j = i + 1

        while j < len(numbers):
            if sum(numbers[i:j]) == invalid:
                print('{} sum to {}'.format(numbers[i:j], invalid))
                srt = sorted(numbers[i:j])
                return srt[0] + srt[-1]
            elif sum(numbers[i:j]) > invalid:
                break

            j += 1

# Part 1
assert find_violation(SAMPLE, 5) == 127

with open('input', 'r') as f:
    SEQUENCE = f.read()

violation = find_violation(SEQUENCE, 25)

# Part 2
assert find_parts(SAMPLE, 127) == 62

parts_sum = find_parts(SEQUENCE, violation)
print('Sum of smallest and largest part: {}'.format(parts_sum))
