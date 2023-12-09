#!/usr/bin/env python3
import argparse
from pathlib import Path
from collections import namedtuple
import numpy as np

FILEPATH = str(Path(__file__).parent / 'input.txt')


def load_txt(filepath) -> list[list[int]]:
    reports = []
    with open(filepath, mode='r') as file:
        for line in file.readlines():
            vals = [int(val) for val in line.strip().rstrip().split(' ')]
            reports.append(vals)
    return reports

def extrapolate_report(report: list[int]) -> int:
    report = np.asarray(report)
    diffs = report[1:] - report[:-1]
    # Only need to sum across the last element of each diff
    last = [report[-1]]
    while not (diffs == 0).all():
        last.append(diffs[-1])
        diffs = diffs[1:] - diffs[:-1]
    return sum(last)

def extrapolate_report_part2(report: list[int]) -> int:
    report = np.asarray(report)
    diffs = report[1:] - report[:-1]
    ret = report[0]
    mult = -1
    while not (diffs == 0).all():
        # To extrapolate backwards, you need to track the multiplier for each diff. The answer is a-b+c-d+e....
        ret += mult * diffs[0]
        mult *= -1
        diffs = diffs[1:] - diffs[:-1]
    return ret

def get_score_part1(reports: list[list[int]]):
    score = 0
    for report in reports:
        score += extrapolate_report(report)
    return score

def get_score_part2(reports: list[list[int]]):
    score = 0
    for report in reports:
        score += extrapolate_report_part2(report)
    return score

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--filepath', type=lambda path: str(Path(path).absolute()), default=FILEPATH)
    pargs = parser.parse_args()
    # part 1
    reports = load_txt(pargs.filepath)
    print(f"Result for part 1: {get_score_part1(reports)}")
    # part 2
    print(f"Result for part 2: {get_score_part2(reports)}")
