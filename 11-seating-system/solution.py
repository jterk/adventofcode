#!/usr/bin/env python
#
# Solution to https://adventofcode.com/2020/day/11
#
import operator

from copy import deepcopy
from functools import reduce
from itertools import product

SAMPLE = '''L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL'''

SAMPLE_TERMINAL = '''#.#L.L#.##
#LLL#LL.L#
L.#.L..#..
#L##.##.L#
#.#L.LL.LL
#.#L#L#.##
..L.L.....
#L#L##L#L#
#.LLLLLL.L
#.#L#L#.##'''

SAMPLE_TERMINAL_VIS = '''#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.LL.L#
#.LLLL#.LL
..#.L.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#'''

def count_occupied_adj(row, col, arrangement):
    min_row = max(0, row - 1)
    max_row = min(len(arrangement) - 1, row + 1)
    min_col = max(0, col - 1)
    max_col = min(len(arrangement[0]) - 1, col + 1)

    locations = [(r, c) for r, c in product(range(min_row, max_row + 1), range(min_col, max_col + 1)) if r != row or c != col]
    # could also use count
    return reduce(lambda x, v: x + v, [1 if arrangement[r][c] == '#' else 0 for r, c in locations])

def is_occupied_vis(row, col, row_fn, col_fn, arrangement):
    # Apply row_fn and col_fn until finding a seat or running out of bounds. Returns True iff a seat
    # is found and it's occupied.
    row = row_fn(row)
    col = col_fn(col)

    while 0 <= row < len(arrangement) and 0 <= col < len(arrangement[0]):
        if arrangement[row][col] == '#':
            return True
        elif arrangement[row][col] == 'L':
            return False

        row = row_fn(row)
        col = col_fn(col)

    # Ran off the edge
    return False

def count_occupied_vis(row, col, arrangement):
    # "Look" in each direction to find first visible seat & determine if it's occupied
    sub = lambda x: x - 1
    add = lambda x: x + 1
    ident = lambda x: x

    dirs = [
        # N
        (sub, ident),
        # NE
        (sub, add),
        # E
        (ident, add),
        # SE
        (add, add),
        # S
        (add, ident),
        # SW
        (add, sub),
        # W
        (ident, sub),
        # NW
        (sub, sub),
    ]

    return [is_occupied_vis(row, col, rf, cf, arrangement) for rf, cf in dirs].count(True)

def find_terminal_arrangement(seats, count_occ_fn, leave_thresh):
    terminal = False
    arrangement = [list(s) for s in seats.split()]
    prev_arrangement = deepcopy(arrangement)

    while not terminal:
        for i, r in enumerate(prev_arrangement):
            for j, s in enumerate(r):
                if s == '.':
                    continue

                if s == 'L' and count_occ_fn(i, j, prev_arrangement) == 0:
                    arrangement[i][j] = '#'
                elif s == '#' and count_occ_fn(i, j, prev_arrangement) >= leave_thresh:
                    arrangement[i][j] = 'L'

        if arrangement == prev_arrangement:
            terminal = True
        else:
            prev_arrangement = deepcopy(arrangement)

    return arrangement

# Part 1
s_term = find_terminal_arrangement(SAMPLE, count_occupied_adj, 4)
assert s_term == [list(s) for s in SAMPLE_TERMINAL.split()]

with open('input', 'r') as f:
    ARRANGEMENT = f.read()

term = find_terminal_arrangement(ARRANGEMENT, count_occupied_adj, 4)
occupied_count = reduce(lambda x, a: x + a.count('#'), term, 0)
assert occupied_count == 2249
print('Part 1: {} seats occupied'.format(occupied_count))

# Part 2
s_term = find_terminal_arrangement(SAMPLE, count_occupied_vis, 5)
assert s_term == [list(s) for s in SAMPLE_TERMINAL_VIS.split()]

term = find_terminal_arrangement(ARRANGEMENT, count_occupied_vis, 5)
occupied_count = reduce(lambda x, a: x + a.count('#'), term, 0)
assert occupied_count = 2023
print('Part 1: {} seats occupied'.format(occupied_count))
