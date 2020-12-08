#!/usr/bin/env python
#
# Solution to https://adventofcode.com/2020/day/8
#

SAMPLE = '''nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6'''

def run_to_loop(instructions, op_ctr=0, acc=0):
    '''Returns a tuple - first value is whether the instructions terminated normally, second is either
    the accumulator at normal termination, or just before the loop was detected.

    '''
    executed = set()

    while op_ctr < len(instructions):
        if op_ctr in executed:
            return (False, acc)

        op, arg = instructions[op_ctr]

        if op == 'acc':
            acc += int(arg)
            executed.add(op_ctr)
            op_ctr += 1
        elif op == 'jmp':
            executed.add(op_ctr)
            op_ctr += int(arg)
        elif op == 'nop':
            executed.add(op_ctr)
            op_ctr += 1

    assert op_ctr == len(instructions)
    return (True, acc)

def run_repair(instructions):
    modified = set()
    op_ctr = 0
    acc = 0

    while True:
        op, arg = instructions[op_ctr]

        if op == 'acc':
            acc += int(arg)
            op_ctr += 1
        elif op == 'jmp':
            if not op_ctr in modified:
                mod_inst = list(instructions)
                mod_inst[op_ctr] = ('nop', arg)
                c, v = run_to_loop(mod_inst, op_ctr, acc)
                modified.add(op_ctr)

                if c:
                    return v

            op_ctr += int(arg)
        elif op == 'nop':
            if not op_ctr in modified:
                mod_inst = list(instructions)
                mod_inst[op_ctr] = ('jmp', arg)
                c, v = run_to_loop(mod_inst, op_ctr, acc)
                modified.add(op_ctr)

                if c:
                    return v

            op_ctr += 1

# Part 1
SAMPLE_INST = []

for line in SAMPLE.split('\n'):
    SAMPLE_INST.append(line.split(' '))

assert run_to_loop(SAMPLE_INST) == (False, 5)

INST = []

with open('input', 'r') as f:
    for line in f:
        INST.append(line.split(' '))
RESULTS_1 = run_to_loop(INST)
assert RESULTS_1 == (False, 2003)
print('Result: {}'.format(RESULTS_1[1]))

# Part 2
assert run_repair(SAMPLE_INST) == 8
print('Repaired result: {}'.format(run_repair(INST)))
