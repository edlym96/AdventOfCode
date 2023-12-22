#!/usr/bin/env python3
import argparse
from pathlib import Path
from collections import namedtuple, defaultdict
from heapq import heappop, heappush

FILEPATH = str(Path(__file__).parent / 'input.txt')

def load_txt(filepath) -> list[list[str]]:
    bricks = []
    with open(filepath, mode='r') as file:
        for line in file.readlines():
            line = line.strip().rstrip()
            point1, point2 = line.split('~')
            point1 = tuple([int(a) for a in point1.split(',')])
            point2 = tuple([int(a) for a in point2.split(',')])
            bricks.append((point1, point2))
    return bricks

def build_support_maps(bricks):
    # Height map of (x,y) -> current highest block on that point
    # height of 0 is the ground, brick index -1 means theres no brick there
    height_map = defaultdict(lambda: (0, -1))

    # brick_index -> set(brick_index)
    supporting = defaultdict(set)
    supported_by = {}

    for brick_idx, brick in enumerate(bricks):
        min_x = min(brick[0][0], brick[1][0])
        max_x = max(brick[0][0], brick[1][0])
        min_y = min(brick[0][1], brick[1][1])
        max_y = max(brick[0][1], brick[1][1])
        min_z = min(brick[0][2], brick[1][2])
        max_z = max(brick[0][2], brick[1][2])

        supported_by_set = set()
        max_height = 0
        # Check x and y, then add supported, supported by
        for i in range(min_x, max_x + 1):
            for j in range(min_y, max_y+1):
                height, prev_brick_idx = height_map[(i, j)]
                if prev_brick_idx == -1:
                    continue
                if height > max_height:
                    max_height = height
                    supported_by_set = set([prev_brick_idx])
                elif height == max_height:
                    supported_by_set.add(prev_brick_idx)
        
        # Add to supporting
        for idx in supported_by_set:
            supporting[idx].add(brick_idx)
        supported_by[brick_idx] = supported_by_set

        # Update height of brick
        for i in range(min_x, max_x + 1):
            for j in range(min_y, max_y+1):
                # new height is z diff + 1 (length of block in z direction) added to max height of the block where it's sitting
                height_map[(i, j)] = (max_z - min_z + 1 + max_height, brick_idx)
    return supporting, supported_by

def solve_part1(bricks) -> int:
    
    supporting, supported_by = build_support_maps(bricks)
    disintegrate = 0
    for i in range(len(bricks)):
        if not len(supporting[i]):
            disintegrate += 1
            continue
        for brick_idx in supporting[i]:
            if len(supported_by[brick_idx]) == 1:
                break
        else:
            disintegrate += 1

    return disintegrate

def solve_part2(bricks) -> int:
    bricks = sorted(bricks, key=lambda brick: min(brick[0][2], brick[1][2]))
    supporting, supported_by = build_support_maps(bricks)
    disintegrate = 0
    for i in range(len(bricks)):
        if not len(supporting[i]):
            continue
        disintegrated = set()
        disintegrated.add(i)
        new_queue = supporting[i]
        while len(new_queue):
            queue = new_queue
            new_queue = set()
            while len(queue):
                brick_idx = queue.pop()
                if not len(supported_by[brick_idx] - disintegrated):
                    disintegrated.add(brick_idx)
                    for brick in supporting[brick_idx]:
                        new_queue.add(brick)
        disintegrate += len(disintegrated) - 1
    return disintegrate

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--filepath', type=lambda path: str(Path(path).absolute()), default=FILEPATH)
    pargs = parser.parse_args()
    # part 1
    bricks = load_txt(pargs.filepath)
    print(f"Result for part 1: {solve_part1(bricks)}")
    # part 2
    print(f"Result for part 2: {solve_part2(bricks)}")
