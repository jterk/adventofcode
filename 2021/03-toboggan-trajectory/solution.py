#!/usr/bin/env python
#
# Solution for part 1 of https://adventofcode.com/2020/day/3
#
sample_rows = [
    '..##.......',
    '#...#...#..',
    '.#....#..#.',
    '..#.#...#.#',
    '.#...##..#.',
    '..#.##.....',
    '.#.#.#....#',
    '.#........#',
    '#.##...#...',
    '#...##....#',
    '.#..#...#.#',
]
sample_result = 7

rows = []
result = 0

def count_trees(rows, x_inc, y_inc):
    pos_x = 0
    pos_y = 0
    trees = 0
    width = len(rows[0])

    while pos_y < len(rows):
        pos_x = (pos_x + x_inc) % width
        pos_y = pos_y + y_inc

        if pos_y < len(rows) and rows[pos_y][pos_x] == '#':
            trees += 1

    return trees

with open('input', 'r') as f:
    # Strip the last empty line from the input
    rows = f.read().split('\n')[:-1]

# part 1
sample_computed = count_trees(sample_rows, 3, 1)
assert(sample_computed == sample_result)

print('part 1 count: {}'.format(count_trees(rows, 3, 1)))

# part 2
sample_product = 1
product = 1

for (x_inc, y_inc) in ((1,1), (3,1), (5,1), (7,1), (1,2)):
    sample_product = sample_product * count_trees(sample_rows, x_inc, y_inc)
    product = product * count_trees(rows, x_inc, y_inc)

assert(sample_product == 336)
print('part 2 product: {}'.format(product))
