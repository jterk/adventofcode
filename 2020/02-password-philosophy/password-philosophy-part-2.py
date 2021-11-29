#!/usr/bin/env python
#
# Solution for part 2 of HTTP://adventofcode.com/2020/day/2
#
# Read `input` read each line with the following format describing a password policy:
#
# M-N C: PASS
#
# * C is the alphabetic character for which the policy is enforced
# * M is the position at which the policy enforcement begins
# * N is the position at which the policy enforcement ends
#
# A password is valid if it contains exactly one instance of C in either position M or position N,
# inclusive. Final output is the number of passwords that passed the corresponding policy.

import re

valid_count = 0
policy_re = re.compile('^(\d+)-(\d+) (\w): (\w+)$')

with open('input', 'r') as f:
    for line in f:
        m = policy_re.match(line)

        if not m:
            print('{} doesn\'t match expected pattern.'.format(line))
            exit(1)

        p1, p2, character, password = m.groups()
        c1 = password[int(p1)-1]
        c2 = password[int(p2)-1]
        if c1 != c2 and (c1 == character or c2 == character):
            print(line)
            valid_count += 1
        else:
            print('{} doesn\'t pass ({})'.format(password, line))

print('{} passwords passed'.format(valid_count))
