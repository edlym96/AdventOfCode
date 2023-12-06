#!/usr/bin/env python3
import argparse
from pathlib import Path
from collections import namedtuple
from functools import reduce

FILEPATH = str(Path(__file__).parent / 'input.txt')
Race = namedtuple('Race', ('time', 'distance'))

def parse_line(line: str, header:str):
    assert line.startswith(header)
    line = line[len(header):].strip().rstrip()
    vals = line.split()
    return vals


def load_txt(filepath) -> list[Race]:
    with open(filepath, mode='r') as file:
        line = file.readline()
        times = parse_line(line, 'Time:')
        line = file.readline()
        distances = parse_line(line, 'Distance:')
    
    return [Race(int(time), int(dist)) for time,  dist in zip(times, distances)]

def load_txt_part2(filepath) -> Race:
    with open(filepath, mode='r') as file:
        line = file.readline()
        times = parse_line(line, 'Time:')
        line = file.readline()
        distances = parse_line(line, 'Distance:')
    
    times = int(''.join(times))
    distances = int(''.join(distances))

    return Race(times, distances)

def calculate_distance(speed, time):
    return speed * time

def find_ways_to_win_race(race: Race):
    low = 0
    # The distance profile is mirrored, so weo nly need to search from the middle
    high = race.time // 2

    # Binary search to find the lowest index where the distance travelled would break the record
    while low != high:
        mid = (low + high) // 2
        dist = calculate_distance(mid, race.time - mid)
        if dist <= race.distance:
            low = mid + 1
        else:
            high = mid
    
    # Can then subtract the two tails from the total time once one is found
    return race.time - (low * 2) + 1

def calculate_score_part1(races):
    races = load_txt(pargs.filepath)
    ways = [find_ways_to_win_race(race) for race in races]
    score = reduce((lambda x, y: x * y), ways)
    return score

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--filepath', type=lambda path: str(Path(path).absolute()), default=FILEPATH)
    pargs = parser.parse_args()
    # part 1
    races = load_txt(pargs.filepath)
    print(f"Result for part 1: {calculate_score_part1(races)}")

    # part 2
    race = load_txt_part2(pargs.filepath)
    print(f"Result for part 2: {find_ways_to_win_race(race)}")
