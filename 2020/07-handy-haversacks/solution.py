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

SAMPLE2= """shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags."""

BAG_SPEC = re.compile('^([a-z ]+) bags contain ([^.]*).$')
CONTAINED_SPEC = re.compile('^([0-9]+) ([a-z ]+) bags?$')

def add_rule(rules, rule_str):
    m = BAG_SPEC.match(rule_str)
    color = m.group(1)
    contains = {}

    assert color not in rules

    for contained in m.group(2).split(', '):
        if contained.startswith('no other'):
            continue

        m = CONTAINED_SPEC.match(contained)
        contains[m.group(2)] = m.group(1)

    rules[color] = contains

def count_containers(rules, color):
    to_check = set([color])
    containers = set()

    while len(to_check):
        contained = to_check.pop()

        for color, contents in rules.items():
            if contained in contents and color not in containers:
                containers.add(color)
                to_check.add(color)

    return len(containers)

def count_contained(rules, color):
    if len(rules[color]):
        subtotal = 0

        for c, count in rules[color].items():
            subtotal += int(count)
            subtotal += int(count) * count_contained(rules, c)

        return subtotal
    else:
        return 0

# Part 1
SAMPLE_RULES = {}

for rule_str in SAMPLE.split('\n'):
    add_rule(SAMPLE_RULES, rule_str)

assert count_containers(SAMPLE_RULES, 'shiny gold') == 4

RULES = {}

with open('input', 'r') as f:
    for l in f:
        add_rule(RULES, l)

containers = count_containers(RULES, 'shiny gold')
print('Bags containing shiny gold: {}'.format(containers))
assert containers == 112

# Part 2
SAMPLE2_RULES = {}

for rule_str in SAMPLE2.split('\n'):
    add_rule(SAMPLE2_RULES, rule_str)

assert count_contained(SAMPLE2_RULES, 'shiny gold') == 126
print('Shiny gold bags contain {} bags'.format(count_contained(RULES, 'shiny gold')))
