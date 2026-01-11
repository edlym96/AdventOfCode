#!/usr/bin/env python3
import argparse
from pathlib import Path
from collections import namedtuple, deque

FILEPATH = str(Path(__file__).parent / 'input.txt')

DIRECTION_DICT = {
    '|': {'v':set([-1, 1])},
    '-': {'h':set([-1, 1])},
    'L': {'h':set([1]), 'v':set([-1])},
    'J': {'h':set([-1]), 'v':set([-1])},
    '7': {'h':set([-1]), 'v':set([1])},
    'F': {'h':set([1]), 'v':set([1])},
    'S': {'h':set([-1, 1]), 'v':set([-1, 1])},
}


def load_txt(filepath) -> list[int]:
    maze = []
    with open(filepath, mode='r') as file:
        for line in file.readlines():
            maze.append(list(line.strip().rstrip()))
    return maze

def find_start(maze):
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            if maze[row][col] == 'S':
                return row, col

def get_steps_of_maze(maze):
    start_row, start_col = find_start(maze)
    steps = [[-1 for _ in range(len(maze[0]))] for k in range(len(maze))]
    step_count = 0
    old_queue = deque([(start_row, start_col, ('h', 1))])
    while len(old_queue):
        new_queue = deque([])
        while len(old_queue):
            row, col, prev_dir = old_queue.popleft()
            # out of bounds
            if row < 0 or row >= len(maze) or col < 0 or col >= len(maze[0]):
                continue
            if steps[row][col] >= 0:
                continue
            symb = maze[row][col]
            if symb == '.':
                continue
            dir_set = DIRECTION_DICT[symb]
            if prev_dir[0] not in dir_set or prev_dir[1] * -1 not in dir_set[prev_dir[0]]:
                continue
            steps[row][col] = step_count
            for dir, possible_set in dir_set.items():
                if dir == 'h':
                    for sign in possible_set:
                        new_queue.append((row, col+(1*sign), ('h', sign)))
                elif dir == 'v':
                    for sign in possible_set:
                        new_queue.append((row+(1*sign), col, ('v', sign)))
        step_count += 1
        old_queue = new_queue
    
    return steps

def count_enclosed_tiles(maze, steps):
    count = 0
    for row in range(len(maze)):
        inside = False
        for col in range(len(maze[0])):
            if maze[row][col] in set(['|', '7', 'F']) and steps[row][col] >= 0:
                inside = not inside
            if inside and steps[row][col] < 0:
                count += 1
    return count
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--filepath', type=lambda path: str(Path(path).absolute()), default=FILEPATH)
    pargs = parser.parse_args()
    # part 1
    maze = load_txt(pargs.filepath)
    steps = get_steps_of_maze(maze)
    print(f"Result for part 1: {max(map(max, steps))}")
    # part 2
    print(f"Result for part 2: {count_enclosed_tiles(maze, steps)}")
