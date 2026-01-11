#!/usr/bin/env python3
import argparse
from pathlib import Path
from collections import namedtuple
from functools import cache

FILEPATH = str(Path(__file__).parent / 'input.txt')

def load_txt(filepath) -> list[list[str]]:
    mirror_maps = []
    with open(filepath, mode='r') as file:
        mp = []
        for line in file.readlines():
            line = line.strip().rstrip()
            if line:
                mp.append(line)
            else:
                mirror_maps.append(mp)
                mp = []
        if len(mp):
            mirror_maps.append(mp)
    return mirror_maps

def string_diff(str1: str, str2: str) -> int:
    count = 0
    for ch1, ch2 in zip(str1, str2):
        if ch1 != ch2:
            count += 1
    return count

def scan_row(mirror_map):
    # handle rows
    for idx in range(len(mirror_map)-1):
        if mirror_map[idx] == mirror_map[idx+1]:
            l = idx - 1
            r = idx + 2
            mirror = True
            while l >= 0 and r < len(mirror_map):
                if mirror_map[l] != mirror_map[r]:
                    mirror = False
                    break
                l -= 1
                r += 1
            if mirror:
                return idx
    return None


"""
for part 2, we only need to count the number of differences when comparing rows/cols
We can allow for a difference of one, but only once when scanning through the mirror map
On top of this, if after the scan we didn't use this allowance, we continue.
"""
def scan_row_part2(mirror_map):
    # handle rows
    for idx in range(len(mirror_map)-1):
        diffs = string_diff(mirror_map[idx], mirror_map[idx+1])
        if diffs < 2:
            allow_one = diffs == 0
            l = idx - 1
            r = idx + 2
            mirror = True
            while l >= 0 and r < len(mirror_map):
                diffs = string_diff(mirror_map[l], mirror_map[r])
                if diffs > 1 or (diffs == 1 and not allow_one):
                    mirror = False
                    break
                if diffs == 1:
                    allow_one = False
                l -= 1
                r += 1
            if allow_one:
                continue
            if mirror:
                return idx
    return None

def scan_col(mirror_map):
    # handle cols
    for idx in range(len(mirror_map[0])-1):
        l_col = ''.join([mirror_map[i][idx] for i in range(len(mirror_map))])
        r_col = ''.join([mirror_map[i][idx+1] for i in range(len(mirror_map))])
        if l_col == r_col:
            l = idx - 1
            r = idx + 2
            mirror = True
            while l >= 0 and r < len(mirror_map[0]):
                l_col = ''.join([mirror_map[i][l] for i in range(len(mirror_map))])
                r_col = ''.join([mirror_map[i][r] for i in range(len(mirror_map))])
                diffs = string_diff(l_col, r_col)
                if l_col != r_col:
                    mirror = False
                    break
                l -= 1
                r += 1
            if mirror:
                return idx
    return None

def scan_col_part2(mirror_map):
    # handle cols
    for idx in range(len(mirror_map[0])-1):
        l_col = ''.join([mirror_map[i][idx] for i in range(len(mirror_map))])
        r_col = ''.join([mirror_map[i][idx+1] for i in range(len(mirror_map))])
        diffs = string_diff(l_col, r_col)
        if diffs < 2:
            allow_one = diffs == 0
            l = idx - 1
            r = idx + 2
            mirror = True
            while l >= 0 and r < len(mirror_map[0]):
                l_col = ''.join([mirror_map[i][l] for i in range(len(mirror_map))])
                r_col = ''.join([mirror_map[i][r] for i in range(len(mirror_map))])
                diffs = string_diff(l_col, r_col)
                if diffs > 1 or (diffs == 1 and not allow_one):
                    mirror = False
                    break
                if diffs == 1:
                    allow_one = False
                l -= 1
                r += 1
            if allow_one:
                continue
            if mirror:
                return idx
    return None

def solve_part1(mirror_maps):
    score = 0
    for mirror_map in mirror_maps:
        multiplier = 100
        row_col = scan_row(mirror_map)
        if row_col is None:
            row_col = scan_col(mirror_map)
            multiplier = 1
        assert row_col is not None
        row_col += 1
        score += row_col * multiplier
    return score

def solve_part2(mirror_maps):
    score = 0
    for mirror_map in mirror_maps:
        multiplier = 100
        row_col = scan_row_part2(mirror_map)
        if row_col is None:
            row_col = scan_col_part2(mirror_map)
            multiplier = 1
        assert row_col is not None
        row_col += 1
        score += row_col * multiplier
    return score

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--filepath', type=lambda path: str(Path(path).absolute()), default=FILEPATH)
    pargs = parser.parse_args()
    # part 1
    mirror_maps = load_txt(pargs.filepath)
    print(f"Result for part 1: {solve_part1(mirror_maps)}")
    # part 2
    print(f"Result for part 2: {solve_part2(mirror_maps)}")
