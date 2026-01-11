#!/usr/bin/env python3
import argparse
from pathlib import Path
from collections import namedtuple
from functools import cache

FILEPATH = str(Path(__file__).parent / 'input.txt')

def load_txt(filepath) -> list[int]:
    path_groups = []
    with open(filepath, mode='r') as file:
        for line in file.readlines():
            path_groups.append(parse_line(line))
    return path_groups

def parse_line(line) -> tuple[str, tuple[int]]:
    path, groups = line.split(' ')
    groups = tuple([int(gr) for gr in groups.split(',')])
    return path, groups

@cache
def recursive_count(path: str, groups: tuple[int]):
    if not len(path):
        return 1 if not len(groups) else 0
    
    # Path could start with '.', '?', '#'
    if path.startswith('.'):
        return recursive_count(path.lstrip('.'), groups)
    
    if path.startswith('#'):
        if len(groups) == 0:
            return 0
        if len(path) < groups[0]:
            return 0
        if any(c == '.' for c in path[:groups[0]]):
            return 0
        if path[groups[0]] == '#':
            return 0
        else:
            return recursive_count(path[groups[0]+1:], groups[1:])

    if path.startswith('?'):
        return recursive_count(path.replace('?', '.', 1), groups) + recursive_count(path.replace('?', '#', 1), groups)

def solve_part1(path_groups):
    total_amount = 0
    for path, groups in path_groups:
        count = recursive_count(path + '.', groups)
        total_amount += count
    return total_amount

def solve_part2(path_groups):
    total_amount = 0
    for path, groups in path_groups:
        count = recursive_count('?'.join([path for _ in range(5)]) + '.', groups * 5)
        total_amount += count
    return total_amount

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--filepath', type=lambda path: str(Path(path).absolute()), default=FILEPATH)
    pargs = parser.parse_args()
    # part 1
    path_groups = load_txt(pargs.filepath)    
    print(f"Result for part 1: {solve_part1(path_groups)}")
    # part 2
    print(f"Result for part 2: {solve_part2(path_groups)}")
