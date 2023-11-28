#!/usr/bin/env python3
from abc import ABC, abstractmethod
import argparse
import copy
from enum import Enum
import heapq
from operator import itemgetter
import re
from typing import Generic, Optional, Tuple, TypeVar, Union

T = TypeVar('T')

'''Base class for each day's implementation.

Fill `PREFIX` with the prefix for that day's inputs, i.e. `'day3'`.

Fill `EXPECTED` with the day's example outputs, i.e. `(1, 42)`.

`_run_impl()` must be implemented for each day, and return the results for parts
1 and 2 in slots 0 and 1 of the returned tuple.'''
class Day(ABC, Generic[T]):
    PREFIX: str
    EXPECTED: Tuple[T, T]

    @abstractmethod
    def _run_impl(self, infile: str) -> Tuple[T, T]:
        raise Exception

    def test(self) -> None:
        r = self._run_impl('{}.example'.format(self.PREFIX))
        assert r == self.EXPECTED, r
        print('Pass')

    def run(self) -> None:
        r = self._run_impl('{}.input'.format(self.PREFIX))
        print('Part 1: {}, Part 2: {}'.format(r[0], r[1]))

DAYS: dict[int, Day] = {}

def main() -> None:
    parser = argparse.ArgumentParser(description='Advent of Code 2022')
    parser.add_argument('day', type=int, choices=range(1,26))
    parser.add_argument('--test', action='store_const', const=True)
    args = parser.parse_args()

    day = args.day - 1
    if day in DAYS:
        if args.test:
            DAYS[day].test()
        else:
            DAYS[day].run()
    else:
        raise Exception('Day {} not implemented'.format(day + 1))

class Day1(Day[int]):
    PREFIX = 'day1'
    EXPECTED = (24000, 45000)

    'Read from `infile` and return a minheap containing the inverse totals of amounts carried by the elves.'
    def make_heap(self, infile: str) -> list[int]:
        with open(infile, 'r') as f:
            h: list[int] = []
            v = 0

            while l := f.readline():
                if l.strip() == '':
                    heapq.heappush(h, -v)
                    v = 0
                else:
                    v += int(l)

            # last value is left without pushing
            heapq.heappush(h, -v)

            return h

    def part1(self, h: list[int]) -> int:
        return -h[0]

    def part2(self, h: list[int]) -> int:
        r = 0

        for _ in range(0, 3):
            r += -heapq.heappop(h)

        return r

    def _run_impl(self, infile: str) -> Tuple[int, int]:
        h = self.make_heap(infile)
        r1 = self.part1(h)
        r2 = self.part2(h)
        return (r1, r2)

class Day2(Day[int]):
    PREFIX = 'day2'
    EXPECTED = (15, 12)

    AGAINST = ['A', 'B', 'C']
    PLAYS = ['X', 'Y', 'Z']

    def _run_impl(self, infile: str) -> Tuple[int, int]:
        pts1 = 0
        pts2 = 0

        with open(infile, 'r') as f:
            while l := f.readline():
                (a, p) = l.split()

                # av, pv are zero-indexed 'against' and 'play' values, math is mod 3
                #
                # av == pv -> draw
                # av == pv + 1 -> win
                # av + 1 == pv -> lose
                av = self.AGAINST.index(a)
                pv = self.PLAYS.index(p)

                # Compute pt 1, where X, Y, Z mean rock, paper, scissors
                pts1 += pv + 1

                if (av + 1) % 3 == pv:
                    pts1 += 6
                elif av == pv:
                    pts1 += 3
                # else lose

                # Now compute pt 2, where X, Y, Z mean lose, draw, win
                pv = (av + pv - 1) % 3
                pts2 += pv + 1

                if (av + 1) % 3 == pv:
                    pts2 += 6
                elif av == pv:
                    pts2 += 3
                # else lose

        return (pts1, pts2)

class Day3(Day[int]):
    PREFIX = 'day3'
    EXPECTED = (157, 70)

    # Map ASCII values to "priority" values from the problem
    def get_dupe_vals(self, dupes: set[int]) -> int:
        dupe_vals = 0

        for dupe in dupes:
            val = dupe - 96

            if val < 0:
                val = dupe - 64 + 26

            dupe_vals += val

        return dupe_vals

    def _run_impl(self, infile: str) -> Tuple[int, int]:
        with open(infile, 'r') as f:
            dupe_vals = 0
            badge_vals = 0

            group = []

            while l := f.readline().strip():
                b = bytes(l, 'ascii')
                group.append(b)

                # part 1 - set intersection within lines
                split = int(len(b) / 2)
                left = b[0:split]
                right = b[split:]

                dupes = set(left).intersection(set(right))
                dupe_vals += self.get_dupe_vals(dupes)

                # part 2 - set intersection within groupings of three lines
                if len(group) == 3:
                    dupes = set(group[0]).intersection(set(group[1]), set(group[2]))
                    assert len(dupes) == 1
                    group = []
                    badge_vals += self.get_dupe_vals(dupes)

            return (dupe_vals, badge_vals)

class Day4(Day[int]):
    PREFIX = 'day4'
    EXPECTED = (2, 4)

    def read_range(self, rs: str) -> Tuple[int, int]:
        (l, r) = rs.split('-')
        return (int(l), int(r))

    def read_range_pair(self, line: str) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        (rs1, rs2) = line.strip().split(',')
        return (self.read_range(rs1), self.read_range(rs2))

    def _run_impl(self, infile: str) -> Tuple[int, int]:
        subsumed = 0
        overlapping = 0

        with open(infile, 'r') as f:
            range_pairs = [self.read_range_pair(l) for l in f]

            for rp in range_pairs:
                # Sort by range start first and negative length second. This
                # puts the shorter range second when both ranges start in the
                # same place, simplifying the overlap test below
                sp = sorted(rp, key=lambda r: (r[0], -r[1]-r[0]))

                if sp[0][1] >= sp[1][0] and sp[0][1] >= sp[1][1]:
                    subsumed += 1

                if sp[1][0] <= sp[0][1]:
                    overlapping += 1

        return (subsumed, overlapping)

class Day5(Day[str]):
    PREFIX = 'day5'
    EXPECTED = ('CMZ', 'MCD')

    STACKS: list[list[str]] = []
    DEEP_STACKS: list[list[str]] = []

    INSTRUCTION_RE = re.compile(r'move (\d+) from (\d+) to (\d+)')

    class Mode(Enum):
        READ_STACKS = 0,
        FIND_INSTRUCTIONS = 1,
        READ_INSTRUCTIONS = 2,

    def _run_impl(self, infile: str) -> Tuple[str, str]:
        with open(infile, 'r') as f:
            mode = Day5.Mode.READ_STACKS

            # Don't strip b/c whitespace is meaningful
            while l := f.readline():
                if mode is Day5.Mode.READ_STACKS:
                    stack_idx = 0

                    while len(l) >= 3:
                        col = l[0:4]
                        l = l[4:]

                        # Make sure to include '\n' since we couldn't strip() earlier
                        val = col.strip(' []\n')

                        # Whwn we've seen a digit we're done reading in the stacks
                        if val.isdigit():
                            for i in range(0, len(self.STACKS)):
                                self.STACKS[i].reverse()

                            self.DEEP_STACKS = copy.deepcopy(self.STACKS)
                            mode = Day5.Mode.FIND_INSTRUCTIONS
                            break

                        if len(self.STACKS) == stack_idx:
                            self.STACKS.append([])

                        if len(val) > 0:
                            assert len(val) == 1
                            self.STACKS[stack_idx].append(val)

                        stack_idx += 1

                elif mode is Day5.Mode.FIND_INSTRUCTIONS:
                    if len(l.strip()) == 0:
                        mode = Day5.Mode.READ_INSTRUCTIONS
                else:
                    m = self.INSTRUCTION_RE.match(l)
                    assert m and len(m.groups()) == 3
                    count = int(m.group(1))
                    fr = int(m.group(2)) - 1
                    to = int(m.group(3)) - 1

                    # part 1, move one at a time
                    for i in range(0, count):
                        val = self.STACKS[fr].pop()
                        self.STACKS[to].append(val)

                    # part 2, move multiple at once
                    i = len(self.DEEP_STACKS[fr])
                    moving = self.DEEP_STACKS[fr][i - count:]
                    self.DEEP_STACKS[fr] = self.DEEP_STACKS[fr][:i - count]
                    self.DEEP_STACKS[to] = self.DEEP_STACKS[to] + moving

            r1 = ''
            r2 = ''

            for stack in self.STACKS:
                r1 = r1 + stack[-1]

            for stack in self.DEEP_STACKS:
                r2 = r2 + stack[-1]

        return (r1, r2)

class Day6(Day[int]):
    PREFIX = 'day6'
    EXPECTED = (7, 19)

    def _run_impl(self, infile: str) -> Tuple[int, int]:
        marker = -1
        msg = -1

        with open(infile, 'r') as f:
            l = f.readline().strip()

            for i in range(0, len(l) - 4):
                chars = set(l[i:i+4])

                if marker == -1 and len(chars) == 4:
                    # marker index is i + 4
                    marker = i + 4

                chars = set(l[i:i+14])

                if msg == -1 and len(chars) == 14:
                    msg = i + 14

                if marker >= 0 and msg >= 0:
                    break

        return (marker, msg)

class Day7(Day[int]):
    PREFIX = 'day7'
    EXPECTED = (95437, -1)

    class Dir():
        name: str
        parent: Optional['Day7.Dir']
        children: list[Union['Day7.Dir', 'Day7.File']]
        _size: Optional[int]

        def __init__(self, parent: Optional['Day7.Dir'], name: str):
            self.children = []
            self.parent = parent
            if self.parent is not None:
                self.parent.add_child(self)
            self.name = name

        def size(self) -> int:
            # memoize to avoid recomputing; assumes child sizes don't change
            if self._size is None:
                self._size = sum([c.size() for c in self.children])

            return self._size

        def add_child(self, child: Union['Day7.Dir', 'Day7.File']):
            self.children.append(child)

        def find_subdir(self, name: str) -> 'Day7.Dir':
            for c in self.children:
                if c.name == name:
                    assert isinstance(c, Day7.Dir)
                    return c

            raise Exception

    class File():
        name: str
        parent: 'Day7.Dir'
        _size: int

        def __init__(self, parent: 'Day7.Dir', name: str, size: int):
            self.name = name
            self.parent = parent
            self.parent.add_child(self)
            self._size = size

        def size(self) -> int:
            return self._size

    def _run_impl(self, infile: str) -> Tuple[int, int]:
        with open(infile, 'r') as f:
            root_dir = Day7.Dir(None, '/')
            current_dir = root_dir

            while l := f.readline().strip():
                if l.startswith('$'):
                    # navigation command; strip first two characters
                    l = l[2:]

                    if l.startswith('cd'):
                        # strip 'cd '; l is now the target
                        l = l[3:]

                        if l == '..':
                            assert current_dir.parent is not None
                            current_dir = current_dir.parent
                        elif l == '/':
                            current_dir = root_dir
                        else:
                            current_dir = current_dir.find_subdir(l)
                    else:
                        # ls, move on to reading contents
                        pass
                else:
                    # content specification for current directory
                    if l.startswith('dir'):
                        dir = Day7.Dir(current_dir, l[4:])
                    else:
                        (ss, name) = l.split()
                        file = Day7.File(current_dir, name, int(ss))

            sizes = []
            current_dir = root_dir
            visited = set()



        return (0, -1)

class DayTemplate(Day[int]):
    PREFIX = ''
    EXPECTED = (-1, -1)

    def _run_impl(self, infile: str) -> Tuple[int, int]:
        return (0, 0)

if __name__ == '__main__':
    DAYS[0] = Day1()
    DAYS[1] = Day2()
    DAYS[2] = Day3()
    DAYS[3] = Day4()
    DAYS[4] = Day5()
    DAYS[5] = Day6()
    DAYS[6] = Day7()
    main()
