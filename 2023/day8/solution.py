#!/usr/bin/env python3
import argparse
import math
from pathlib import Path
from collections import namedtuple

FILEPATH = str(Path(__file__).parent / 'input.txt')
START_NODE = "AAA"
END_NODE = "ZZZ"

class Node:
    def __init__(self, index, left, right):
        self.index = index
        self.left = left
        self.right = right

def parse_line(line: str) -> Node:
    index, left_right = line.split('=')
    index = index.strip().rstrip()
    left_right = left_right.strip().rstrip()
    left, right = left_right[1:-1].split(', ')
    return Node(index, left, right)


def load_txt(filepath) -> list[int]:
    nodes = {}
    with open(filepath, mode='r') as file:
        instructions = file.readline()
        instructions = instructions.strip().rstrip()
        file.readline()
        for line in file.readlines():
            node = parse_line(line)
            if node.index in nodes:
                raise ValueError("Duplicate node found in input")
            nodes[node.index] = node
    return instructions, nodes

def iter_instructions(instructions):
    i = 0
    while True:
        yield instructions[i % len(instructions)]
        i += 1

def traverse_part1(instructions, nodes):
    curr_node = nodes[START_NODE]
    steps = 0
    for instruction in iter_instructions(instructions):
        if curr_node.index == END_NODE:
            return steps
        if instruction == 'L':
            curr_node = nodes[curr_node.left]
        elif instruction == 'R':
            curr_node = nodes[curr_node.right]
        else:
            raise ValueError(f"Unexpected instruction {instruction}")
        steps += 1

"""
This solution uses LCM of each node after it has reached the end. This solution only works because each end-node is cyclical.
In reality, there could be some offset from **A -> **Z , and you would also need to find a solution for each **Z -> **Z cycle.
In this case, the input is nicely formed so each **Z -> **Z ycle traverses back to itself and the initial **A -> **Z traverse has the same number of steps.
"""
def traverse_part2(instructions, nodes):
    curr_nodes = [node_idx for node_idx in nodes.keys() if node_idx.endswith('A')]
    steps = []
    for node in curr_nodes:
        curr_node = node
        curr_steps = 0
        for instruction in iter_instructions(instructions):
            if curr_node.endswith('Z'):
                steps.append(curr_steps)
                break
            if instruction == 'L':
                curr_node = nodes[curr_node].left
            elif instruction == 'R':
                curr_node = nodes[curr_node].right
            else:
                raise ValueError(f"Unexpected instruction {instruction}")
            curr_steps += 1
    return math.lcm(*steps)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--filepath', type=lambda path: str(Path(path).absolute()), default=FILEPATH)
    pargs = parser.parse_args()
    # part 1
    instructions, nodes = load_txt(pargs.filepath)
    print(f"Result for part 1: {traverse_part1(instructions, nodes)}")
    # part 2
    print(f"Result for part 2: {traverse_part2(instructions, nodes)}")
