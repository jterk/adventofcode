#!/usr/bin/env python
#
# Solution for
#
SAMPLE1 = '''16
10
15
5
1
11
7
19
6
12
4'''

SAMPLE2 = '''28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3'''

def count_differences(adapters):
    differences = {
        1: 0,
        3: 0,
    }

    for i, v in enumerate(adapters):
        if i > 0:
            if v - adapters[i - 1] == 1:
                differences[1] += 1
            elif v - adapters[i - 1] == 3:
                differences[3] += 1
        else:
            # Difference from 0 -> first adapter
            if v == 1:
                differences[1] += 1
            elif v == 3:
                differences[3] += 1

    # Difference from last adapter -> device
    differences[3] += 1
    return differences

def count_configs(adapters):
    r_adapters = list(adapters)
    r_adapters.reverse()
    # Account for multiple ways to start from 0
    r_adapters.append(0)
    paths_starting_at = {}

    for i, v in enumerate(r_adapters):
        paths_starting_at[v] = 0

        if i == 0:
            # One path from terminal adapter to device
            paths_starting_at[v] = 1
            continue

        for t in reversed(r_adapters[0:i]):
            if 1 <= t - v <= 3:
                # t is reachable from v
                #print('Looking at {} from {}'.format(t, v))
                assert t in paths_starting_at, 'Missing path for {}'.format(t)
                paths_starting_at[v] += paths_starting_at[t]
            elif t - v > 3:
                # no more reachable nodes
                break

    return paths_starting_at[0]

# Part 1
A1 = sorted(int(i) for i in SAMPLE1.split())
A2 = sorted(int(i) for i in SAMPLE2.split())

assert count_differences(A1) == {1: 7, 3: 5}
assert count_differences(A2) == {1: 22, 3:10}

with open('input', 'r') as f:
    ADAPTERS = sorted(int(i) for i in f)

differences = count_differences(ADAPTERS)
print(differences)
print('P1: {}'.format(differences[1] * differences[3]))

# Part 2
assert count_configs(A1) == 8
assert count_configs(A2) == 19208

configs = count_configs(ADAPTERS)
print('P2: {}'.format(configs))
