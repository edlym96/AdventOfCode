#!/usr/bin/env python3
import argparse
from pathlib import Path

FILEPATH = str(Path(__file__).parent / 'input.txt')

DIGIT_MAP = {
    'one': "1",
    'two': "2",
    'three': "3",
    'four': "4",
    'five': "5",
    'six': "6",
    'seven': "7",
    'eight': "8",
    'nine': '9',
}

def find_first(line: str):
    for i in range(len(line)):
        if line[i].isnumeric():
            return i
    else:
        raise ValueError(f"No digit found for {line}")

def find_first_part2(line:str):
    # Find first spelled
    min_idx = float('inf')
    str_val = None
    for digit_str, digit in DIGIT_MAP.items():
        digit_idx = line.find(digit_str)
        if digit_idx < 0:
            continue
        if digit_idx < min_idx:
            str_val = digit
            min_idx = digit_idx

    # Find first numeric digit
    try:
        num_idx = find_first(line)
    except ValueError:
        num_idx = float('inf')

    # return either the numeric or the spelled digit depending on which came first
    if num_idx < min_idx:
        return line[num_idx]
    else:
        assert str_val is not None
        return str_val


def find_last(line: str):
    for i in range(len(line)-1, -1, -1):
        if line[i].isnumeric():
            return i
    else:
        raise ValueError(f"No digit found for {line}")

def find_last_part2(line:str):
    # Find last spelled digit
    max_idx = -1
    str_val = None
    for digit_str, digit in DIGIT_MAP.items():
        digit_idx = line.rfind(digit_str)
        if digit_idx > max_idx:
            str_val = digit
            max_idx = digit_idx

    # Find last numeric digit
    try:
        num_idx = find_last(line)
    except ValueError:
        num_idx = -1
    
    # return either the numeric or spelled digit depending on which came last
    if num_idx > max_idx:
        return line[num_idx]
    else:
        assert str_val is not None
        return str_val


def load_txt(filepath) -> list[int]:
    digits = []
    with open(filepath, mode='r') as file:
        for line in file.readlines():
            line = line.strip().rstrip()
            first, last = line[find_first(line)], line[find_last(line)]
            total = first + last
            digits.append(int(total))
    return digits
            
def load_txt_part2(filepath) -> list[int]:
    digits = []
    with open(filepath, mode='r') as file:
        for line in file.readlines():
            line = line.strip().rstrip()
            first, last = find_first_part2(line), find_last_part2(line)
            total = first + last
            digits.append(int(total))
    return digits

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--filepath', type=lambda path: str(Path(path).absolute()), default=FILEPATH)
    pargs = parser.parse_args()
    # part 1
    values = load_txt(pargs.filepath)
    print(f"Result for part 1: {sum(values)}")
    # part 2
    values = load_txt_part2(pargs.filepath)
    print(f"Result for part 2: {sum(values)}")
