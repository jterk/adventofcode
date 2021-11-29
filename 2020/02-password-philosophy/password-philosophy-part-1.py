#!/usr/bin/env python
#
# Solution for part 1 of https://adventofcode.com/2020/day/2
#
# Read `input` read each line with the following format describing a password policy:
#
# M-N C: PASS
#
# * C is the alphabetic character for which the policy is enforced
# * M is the minimum number of times C must appear in PASS
# * N is the maximum number of times C may appear in PASS
#
# Final output is the number of passwords that passed the corresponding policy.
import re

valid_count = 0
policy_re = re.compile('^(\d+)-(\d+) (\w): (\w+)$')

with open('input', 'r') as f:
    for line in f:
        m = policy_re.match(line)

        if not m:
            print('{} doesn\'t match expected pattern.'.format(line))
            exit(1)

        min_count, max_count, character, password = m.groups()
        count = password.count(character)

        if count < int(min_count) or count > int(max_count):
            print('{} does not have between {} and {} instances of {}'.format(
                password, min_count, max_count, character))
        else:
            valid_count += 1

print('{} passwords passed'.format(valid_count))
