#!/usr/bin/env python
#
# Solution to https://adventofcode.com/2020/day/5
#
import re

PASS_PATTERN = re.compile('^([FB]{7})([RL]{3})$')

# Decodes a pass string in the format described here:
#
# The first 7 characters will either be F or B; these specify exactly one of the 128 rows on the
# plane (numbered 0 through 127). Each letter tells you which half of a region the given seat is
# in. Start with the whole list of rows; the first letter indicates whether the seat is in the front
# (0 through 63) or the back (64 through 127). The next letter indicates which half of that region
# the seat is in, and so on until you're left with exactly one row.
#
# For example, consider just the first seven characters of FBFBBFFRLR:
#
#     Start by considering the whole range, rows 0 through 127.
#     F means to take the lower half, keeping rows 0 through 63.
#     B means to take the upper half, keeping rows 32 through 63.
#     F means to take the lower half, keeping rows 32 through 47.
#     B means to take the upper half, keeping rows 40 through 47.
#     B keeps rows 44 through 47.
#     F keeps rows 44 through 45.
#     The final F keeps the lower of the two, row 44.
#
# The last three characters will be either L or R; these specify exactly one of the 8 columns of
# seats on the plane (numbered 0 through 7). The same process as above proceeds again, this time
# with only three steps. L means to keep the lower half, while R means to keep the upper half.
#
# For example, consider just the last 3 characters of FBFBBFFRLR:
#
#     Start by considering the whole range, columns 0 through 7.
#     R means to take the upper half, keeping columns 4 through 7.
#     L means to take the lower half, keeping columns 4 through 5.
#     The final R keeps the upper of the two, column 5.
#
# So, decoding FBFBBFFRLR reveals that it is the seat at row 44, column 5.
#
# Every seat also has a unique seat ID: multiply the row by 8, then add the column. In this example,
# the seat has ID 44 * 8 + 5 = 357.
#
# Returns a dict with three attributes: `row`, `column`, `seat_id`
def decode_pass(pas):
    m = PASS_PATTERN.match(pas)

    if not m:
        print('{} does not match expected pattern'.format(pas))
        exit(-1)

    row_spec, col_spec = m.groups()
    min_row, max_row = 0, 127

    for r in row_spec:
        #print(r)
        min_row, max_row = halve_interval(r, 'F', 'B', min_row, max_row)
        #print('{} min {} max {}'.format(r, min_row, max_row))

    assert(min_row == max_row)

    min_col, max_col = 0, 7

    for c in col_spec:
        #print(c)
        min_col, max_col = halve_interval(c, 'L', 'R', min_col, max_col)
        #print('{} min {} max {}'.format(c, min_col, max_col))

    assert(min_col == max_col)

    return {
        'row': min_row,
        'column': min_col,
        'seat_id': min_row * 8 + min_col
    }

# Halve the interval between `low_val` and `hi_val` by inspecting `c`. If `c == l`, use the lower
# half of the interval, otherwise use the upper half. Returns a new `(low_val, hi_val)` tuple.
def halve_interval(c, l, r, low_val, hi_val):
    if c == l:
        hi_val = int((hi_val + low_val + 1) / 2 -1)
    else:
        low_val = int((hi_val + low_val + 1) / 2)

    return (low_val, hi_val)

# Part 1
SAMPLES = {
    'FBFBBFFRLR': {
        'row': 44,
        'column': 5,
        'seat_id': 357,
    },
    'BFFFBBFRRR': {
        'row': 70,
        'column': 7,
        'seat_id': 567,
    },
    'FFFBBBFRRR': {
        'row': 14,
        'column': 7,
        'seat_id': 119,
    },
    'BBFFBBFRLL': {
        'row': 102,
        'column': 4,
        'seat_id': 820,
    },
}

for pas, expected in SAMPLES.items():
    decoded = decode_pass(pas)
    assert expected == decoded, '{} != {}'.format(expected, decoded)

decoded_passes = []
max_id = -1

with open('input', 'r') as f:
    for pas in f:
        decoded = decode_pass(pas)
        decoded_passes.append(decoded)

        if decoded['seat_id'] > max_id:
            max_id = decoded['seat_id']

print('Max ID: {}'.format(max_id))

# Part 2
decoded_passes.sort(key=lambda v : v['seat_id'])
for i, pas in enumerate(decoded_passes):
    if decoded_passes[i + 1]['seat_id'] == pas['seat_id'] + 2:
        print('Missing seat ID: {}'.format(pas['seat_id'] + 1))
        exit(0)
