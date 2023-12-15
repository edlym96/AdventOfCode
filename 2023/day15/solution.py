#!/usr/bin/env python3
import argparse
from pathlib import Path
from collections import namedtuple
from functools import cache

FILEPATH = str(Path(__file__).parent / 'input.txt')

def load_txt(filepath) -> list[str]:
    with open(filepath, mode='r') as file:
        line = file.readline()
        line = line.strip().rstrip()
        init_squence = line.split(',')
    return init_squence

class Node:

    def __init__(self, val, prev, nxt):
        self.val = val
        self.prev = prev
        self.next = nxt

class Box:
    """
    Box contains a doubly linked list for the lenses and a dict for tracking label to lens
    """
    def __init__(self, index):
        self.index = index
        self.label_to_lens = {}
        self.head = None
        self.tail = None
    
    def remove(self, label):
        if label not in self.label_to_lens:
            return
        lens = self.label_to_lens[label]
        if lens.prev:
            lens.prev.next = lens.next
        else:
            # Handle lens is head
            self.head = lens.next
        if lens.next:
            lens.next.prev = lens.prev
        else:
            # Handle lens is tail
            self.tail = lens.prev

        del self.label_to_lens[label]
    
    def add(self, label, focal_length):
        if label in self.label_to_lens:
            self.label_to_lens[label].val = focal_length
            return
        # If linked list is not empty, add to tail
        if self.tail is not None:
            node = Node(focal_length, self.tail, None)
            self.tail.next = node
        else:
            # Else, add to both head and tail
            node = Node(focal_length, None, None)
            self.head = node
        self.tail = node
        self.label_to_lens[label] = node
    
    def calc_score(self):
        curr = self.head
        mult = 1
        score = 0
        while curr != None:
            score += curr.val * mult
            mult += 1
            curr = curr.next
        return score * (self.index + 1)

def calc_hash(string: str):
    hash = 0
    for char in string:
        ascii = ord(char)
        hash += ascii
        hash *= 17
        hash = hash % 256
    return hash

def solve_part1(init_sequence: list[str]):
    score = 0

    for seq in init_sequence:
        score += calc_hash(seq)

    return score

def solve_part2(init_sequence: list[str]):
    score = 0

    boxes = [Box(i) for i in range(256)]

    for seq in init_sequence:
        # add
        if '=' in seq:
            label, focal_length = seq.split('=')
            focal_length = int(focal_length)
            hash = calc_hash(label)
            boxes[hash].add(label, focal_length)
        elif '-' in seq:
            label = seq[:-1]
            hash = calc_hash(label)
            boxes[hash].remove(label)
    
    for box in boxes:
        score += box.calc_score()

    return score

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--filepath', type=lambda path: str(Path(path).absolute()), default=FILEPATH)
    pargs = parser.parse_args()
    # part 1
    init_squence = load_txt(pargs.filepath)
    print(f"Result for part 1: {solve_part1(init_squence)}")
    # part 2
    print(f"Result for part 2: {solve_part2(init_squence)}")
