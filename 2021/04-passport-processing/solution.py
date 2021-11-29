#!/usr/bin/env python
#
# Solution for https://adventofcode.com/2020/day/4
#
import re

sample_input = """
ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
"""

sample_valid_count = 2

def parse_input(lines):
    passports = []
    passport = {}

    for line in lines:
        if len(line) == 0:
            passports.append(passport)
            passport = {}
        else:
            fields = line.split(' ')

            for field in fields:
                passport[field.split(':')[0]] = field.split(':')[1]

    return passports

def is_valid(passport):
    required_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

    for field in required_fields:
        if field not in passport.keys():
            return False

    return True

height_re = re.compile('^(\d{2,3})(cm|in)$')

def is_valid_height(v):
    m = height_re.match(v)

    return m and (
        (m.group(2) == 'cm' and int(m.group(1)) >= 150 and int(m.group(1)) <= 193) or
        (m.group(2) == 'in' and int(m.group(1)) >= 59 and int(m.group(1)) <= 76))

def is_valid2(passport):
    year_re = re.compile('^\d{4}$')

    field_validators = {
        'byr': lambda v : year_re.match(v) and int(v) >= 1920 and int(v) <= 2002,
        'iyr': lambda v : year_re.match(v) and int(v) >= 2010 and int(v) <= 2020,
        'eyr': lambda v : year_re.match(v) and int(v) >= 2020 and int(v) <= 2030,
        'hgt': is_valid_height,
        'hcl': lambda v : re.match('^#[\da-f]{6}$', v),
        'ecl': lambda v : v in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'],
        'pid': lambda v : re.match('^\d{9}$', v),
    }

    for k in field_validators.keys():
        if not k in passport or not field_validators[k](passport[k]):
            return False

    return True

def count_valid(passports, fn):
    valid = 0

    for passport in passports:
        if fn(passport):
            valid += 1

    return valid

# Part 1
sample_passports = parse_input(sample_input.split('\n'))
print(sample_passports)
print(len(sample_passports))

sample_valid = count_valid(sample_passports, is_valid)
print(sample_valid)
assert(sample_valid == 2)

with open('input', 'r') as file:
    passports = parse_input(file.read().split('\n'))
    valid_count = count_valid(passports, is_valid)
    print('{} valid'.format(valid_count))

    valid2_count = count_valid(passports, is_valid2)
    print('{} valid for part 2'.format(valid2_count))

# Part 2
