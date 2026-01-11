#!/usr/bin/env python3
import argparse
from pathlib import Path
from collections import defaultdict
from copy import deepcopy

FILEPATH = str(Path(__file__).parent / 'input.txt')

def load_txt(filepath) -> list[list[str]]:
    maze = []
    with open(filepath, mode='r') as file:
        for line in file.readlines():
            maze.append(list(line.strip().rstrip()))
    return maze

def find_start(maze):
    for i in range(len(maze[0])):
        if maze[0][i] == '.':
            return i

def find_end(maze):
    for i in range(len(maze[0])):
        if maze[-1][i] == '.':
            return i

def recurse_traverse(maze, row, col, visited, count, end_col):
    possible_steps = []        
    max_steps = 0
    if row == (len(maze) - 1) and col == end_col:
        max_steps = max(max_steps, count)
        return max_steps
    
    visited.add((row, col))
    if maze[row][col] == '>':
        if 0 <= col + 1 < len(maze[0]) and (row, col+1) not in visited and maze[row][col+1] != '#':
            possible_steps.append((row, col+1))
    elif maze[row][col] == '<':
        if 0 <= col -1 < len(maze[0]) and (row, col-1) not in visited and maze[row][col-1] != '#':
            possible_steps.append((row, col-1))
    elif maze[row][col] == 'v':
        if 0 <= row + 1 < len(maze) and (row+1, col) not in visited and maze[row+1][col] != '#':
            possible_steps.append((row+1, col))
    elif maze[row][col] == '^':
        if 0 <= row -1 < len(maze) and (row-1, col) not in visited and maze[row-1][col] != '#':
            possible_steps.append((row-1, col))
    else:
        if 0 <= row + 1 < len(maze) and (row+1, col) not in visited  and maze[row+1][col] != '#':
            possible_steps.append((row+1, col))
        if 0 <= row -1 < len(maze) and (row-1, col) not in visited  and maze[row-1][col] != '#':
            possible_steps.append((row-1, col))
        if 0 <= col + 1 < len(maze[0]) and (row, col+1) not in visited and maze[row][col+1] != '#':
            possible_steps.append((row, col+1))
        if 0 <= col -1 < len(maze[0]) and (row, col-1) not in visited and maze[row][col-1] != '#':
            possible_steps.append((row, col-1))

    
    while len(possible_steps) == 1:
        curr_row, curr_col = possible_steps.pop()
        visited.add((curr_row, curr_col))
        count += 1
        if curr_row == (len(maze) - 1) and curr_col == end_col:
            max_steps = max(max_steps, count)
            continue

        if maze[curr_row][curr_col] == '>':
            if 0 <= curr_col + 1 < len(maze[0]) and (curr_row, curr_col+1) not in visited and maze[curr_row][curr_col+1] != '#':
                possible_steps.append((curr_row, curr_col+1))
        elif maze[curr_row][curr_col] == '<':
            if 0 <= curr_col -1 < len(maze[0]) and (curr_row, curr_col-1) not in visited and maze[curr_row][curr_col-1] != '#':
                possible_steps.append((curr_row, curr_col-1))
        elif maze[curr_row][curr_col] == 'v':
            if 0 <= curr_row + 1 < len(maze) and (curr_row+1, curr_col) not in visited and maze[curr_row+1][curr_col] != '#':
                possible_steps.append((curr_row+1, curr_col))
        elif maze[curr_row][curr_col] == '^':
            if 0 <= curr_row -1 < len(maze) and (curr_row-1, curr_col) not in visited and maze[curr_row-1][curr_col] != '#':
                possible_steps.append((curr_row-1, curr_col))
        else:
            if 0 <= curr_row + 1 < len(maze) and (curr_row+1, curr_col) not in visited  and maze[curr_row+1][curr_col] != '#':
                possible_steps.append((curr_row+1, curr_col))
            if 0 <= curr_row -1 < len(maze) and (curr_row-1, curr_col) not in visited  and maze[curr_row-1][curr_col] != '#':
                possible_steps.append((curr_row-1, curr_col))
            if 0 <= curr_col + 1 < len(maze[0]) and (curr_row, curr_col+1) not in visited and maze[curr_row][curr_col+1] != '#':
                possible_steps.append((curr_row, curr_col+1))
            if 0 <= curr_col -1 < len(maze[0]) and (curr_row, curr_col-1) not in visited and maze[curr_row][curr_col-1] != '#':
                possible_steps.append((curr_row, curr_col-1))
    
    if len(possible_steps):
        for r,c in possible_steps:
            max_steps = max(max_steps, recurse_traverse(maze, r, c, deepcopy(visited), count + 1, end_col))
    
    return max_steps


def solve_part1(maze, start_col, end_col) -> int:
    
    visited = set()

    return recurse_traverse(maze, 0, start_col, visited, 0, end_col)

def adj(maze, row, col):
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for dx, dy in dirs:
        n_row = row + dx
        n_col = col + dy
        if n_row < 0 or n_row >= len(maze) or n_col < 0 or n_col >= len(maze[0]):
            continue
        if maze[n_row][n_col] != '#':
            yield (n_row, n_col)

def solve_part2(maze, start_col, end_col) -> int:
    vertices = set()
    graph = defaultdict(list)

    # Get all nodes with multiple paths ie > 2
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] != "#":
                n_adj = len(list(adj(maze, i,j)))
                if n_adj > 2:
                    vertices.add((i,j))
    vertices.add((0,start_col))
    vertices.add((len(maze)-1,end_col))

    # Build the graph of node to node along with the distances
    for x,y in vertices:
        q = []
        q.append((x,y))
        seen = {(x,y)}
        dist = 0
        while len(q) > 0:
            nq = []
            dist += 1
            for c in q:
                for a in adj(maze, *c):
                    if a not in seen:
                        if a in vertices:
                            graph[(x,y)].append((dist, a))
                            seen.add(a)
                        else:
                            seen.add(a)
                            nq.append(a)
            q = nq

    # dfs through the graph to find the longest
    best = 0
    def dfs(cur, pathset, totaldist):
        nonlocal best
        if cur == (len(maze)-1,end_col):
            if totaldist > best:
                best = max(best, totaldist)
        for da,a in graph[cur]:
            if a not in pathset:
                pathset.add(a)
                dfs(a,pathset, totaldist + da)
                pathset.remove(a)

    dfs((0,1), set(), 0)
    return best

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--filepath', type=lambda path: str(Path(path).absolute()), default=FILEPATH)
    pargs = parser.parse_args()
    # part 1
    maze = load_txt(pargs.filepath)
    start_col = find_start(maze)
    end_col = find_end(maze)
    print(f"Result for part 1: {solve_part1(maze, start_col, end_col)}")
    # part 2
    print(f"Result for part 2: {solve_part2(maze, start_col, end_col)}")
