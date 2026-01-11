#!/usr/bin/env python3
import argparse
from pathlib import Path
from collections import namedtuple, deque
from heapq import heappop, heappush
from typing import Any

FILEPATH = str(Path(__file__).parent / 'input.txt')

class GreaterThan:
    def __init__(self, char, comparison_val):
        self.char = char
        self.comparison_val = comparison_val
        self.comparison_char = '>'

    def __call__(self, part) -> bool:
        if self.char not in part:
            return False
        return part[self.char] > self.comparison_val
    
class LessThan:
    def __init__(self, char, comparison_val):
        self.char = char
        self.comparison_val = comparison_val
        self.comparison_char = '<'

    def __call__(self, part) -> bool:
        if self.char not in part:
            return False
        return part[self.char] < self.comparison_val

class Workflow:

    def __init__(self, input_strings: list[str]):
        self.conditions = []
        for input_str in input_strings[:-1]:
            condition_str, return_val = input_str.split(':')
            char = condition_str[0]
            comparator_str = condition_str[1]
            comparison_val = int(condition_str[2:])
            if comparator_str == '>':
                condition_class = GreaterThan
            else:
                condition_class = LessThan
            self.conditions.append((condition_class(char, comparison_val), return_val))
        self._terminal_val = input_strings[-1]

    def process_part(self, part)->str:
        for fn, next_val in self.conditions:
            if fn(part):
                return next_val
        else:
            return self._terminal_val
    
    def process_range(self, xl, xh, ml, mh, al, ah, sl, sh):
        return_ranges = []
        for fn, next_val in self.conditions:
            new_xl, new_xh, new_ml, new_mh, new_al, new_ah, new_sl, new_sh = xl, xh, ml, mh, al, ah, sl, sh
            if fn.char == 'x':
                l,h = xl, xh
                inverted_l, inverted_h = xl, xh
            elif fn.char == 'm':
                l,h = ml, mh
                inverted_l, inverted_h = ml, mh
            elif fn.char == 'a':
                l,h = al, ah
                inverted_l, inverted_h = al, ah
            else:
                l,h = sl, sh
                inverted_l, inverted_h = sl, sh

            if fn.comparison_char == '>':
                if l <= fn.comparison_val:
                    l = fn.comparison_val + 1
                    inverted_h = fn.comparison_val
            else:
                if h >= fn.comparison_val:
                    h = fn.comparison_val - 1
                    inverted_l = fn.comparison_val

            if fn.char == 'x':
                new_xl, new_xh = l, h
                xl, xh = inverted_l, inverted_h
            elif fn.char == 'm':
                new_ml, new_mh = l, h
                ml, mh = inverted_l, inverted_h
            elif fn.char == 'a':
                new_al, new_ah = l, h
                al, ah = inverted_l, inverted_h
            else:
                new_sl, new_sh = l, h
                sl, sh = inverted_l, inverted_h
            return_ranges.append((next_val, new_xl, new_xh, new_ml, new_mh, new_al, new_ah, new_sl, new_sh))
        return_ranges.append((self._terminal_val, xl, xh, ml, mh, al, ah, sl, sh))
        return return_ranges
        
def load_txt(filepath) -> list[list[str]]:
    workflows = {}
    parts = []
    with open(filepath, mode='r') as file:
        line = file.readline()
        line = line.strip().rstrip()
        while len(line):
            f_start = line.find('{')
            workflow_name = line[:f_start]
            conditions = line[f_start+1:-1]
            conditions = conditions.split(',')
            workflows[workflow_name] = Workflow(conditions)
            line = file.readline()
            line = line.strip().rstrip()
        
        line = file.readline()
        line = line.strip().rstrip()
        while (len(line)):
            specs = line[1:-1].split(',')
            rec = {}
            for spec in specs:
                char, val = spec.split('=')
                val = int(val)
                rec[char] = val
            parts.append(rec)
            line = file.readline()
            line = line.strip().rstrip()        
    return workflows, parts

def process_part(workflows, part):
    curr_workflow = 'in'
    while curr_workflow not in {'R', 'A'}:
        curr_workflow = workflows[curr_workflow].process_part(part)
    assert curr_workflow in {'R', 'A'}
    return curr_workflow == 'A'

def solve_part1(workflows, parts) -> int:
    accepted_parts = []
    for part in parts:
        if process_part(workflows, part):
            accepted_parts.append(part)

    total = 0
    for a_part in accepted_parts:
        total += sum(a_part.values())
    return total

def solve_part2(workflows) -> int:
    
    queue = deque([('in', 1, 4000, 1, 4000, 1, 4000, 1, 4000)])
    total = 0
    while len(queue):
        curr_workflow, xl, xh, ml, mh, al, ah, sl, sh = queue.pop()
        if xl > xh or ml > mh or al > ah or sl > sh:
            continue
        if curr_workflow == 'A':
            total += (xh-xl+1)*(mh-ml+1)*(ah-al+1)*(sh-sl+1)
        elif curr_workflow == 'R':
            continue
        else:
            new_ranges = workflows[curr_workflow].process_range(xl, xh, ml, mh, al, ah, sl, sh)
            for new_range in new_ranges:
                queue.append(new_range)
    return total

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--filepath', type=lambda path: str(Path(path).absolute()), default=FILEPATH)
    pargs = parser.parse_args()
    # part 1
    workflows, parts = load_txt(pargs.filepath)
    print(f"Result for part 1: {solve_part1(workflows, parts)}")
    # part 2
    print(f"Result for part 2: {solve_part2(workflows)}")
