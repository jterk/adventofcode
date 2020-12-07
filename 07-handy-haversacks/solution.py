#!/usr/bin/env python
#
# Solution for https://adventofcode.com/2020/day/7
#
import re

SAMPLE = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""

class Bag:
    def __init__(self, color):
        self.color = color
        self.contains = dict()
        self.contained_by = set()

    def __str__(self):
        return self.color

    def __hash__(self):
        return hash(self.color)

    def add_container(self, container):
        #print('Adding container {} for {}'.format(container.color, self.color))
        self.contained_by.add(container)
        #print(self.contained_by)

    def add_contents(self, contained, count):
        self.contains[contained] = count

    def containers(self):
        return self.contained_by

class BagColors:
    BAG_SPEC = re.compile('^([a-z ]+) bags contain ([^.]*).$')
    CONTAINED_SPEC = re.compile('^([0-9]+) ([a-z ]+) bags?$')

    bags = dict()

    def add_bag(self, input_line):
        #print(input_line)
        m = self.BAG_SPEC.match(input_line)
        #print(m)
        #print(m.group(2).split(', '))

        if not m:
            print('{} does not match expected spec'.format(input_line))
            exit(1)

        color = m.group(1)

        if not color in self.bags:
            self.bags[color] = Bag(color)

        for contained in m.group(2).split(', '):
            if contained.startswith('no other'):
                continue

            m = self.CONTAINED_SPEC.match(contained)

            if not m:
                print('{} does not match expected contained spec'.format(contained))
                exit(1)

            c_count = m.group(1)
            c_color = m.group(2)

            #print('{} contains {} {}'.format(color, c_count, c_color))

            if not c_color in self.bags:
                self.bags[c_color] = Bag(c_color)

            self.bags[c_color].add_container(self.bags[color])
            self.bags[color].add_contents(self.bags[c_color], c_count)

    def add_bags(self, input_lines):
        for l in input_lines.split('\n'):
            self.add_bag(l)

    def get_containers(self, color):
        # Needs to be turned into a loop for real soln
        bag = self.bags[color]
        assert bag
        #print(color)
        #print([b.color for b in bag.containers()])

        if not len(bag.containers()):
            return {bag}
        else:
            containers = set()

            for b in bag.containers():
                containers.update({b})
                containers.update(self.get_containers(b.color))

            return containers

# Part 1
SAMPLE_BAGS = BagColors()
SAMPLE_BAGS.add_bags(SAMPLE)
assert len(SAMPLE_BAGS.get_containers('shiny gold')) == 4

BAGS = BagColors()

with open('input', 'r') as f:
    for l in f:
        BAGS.add_bag(l)

print('Bags containing shiny gold: {}'.format(len(BAGS.get_containers('shiny gold'))))
