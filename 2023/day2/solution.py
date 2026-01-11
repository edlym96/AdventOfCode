#!/usr/bin/env python3
import argparse
from pathlib import Path
from collections import namedtuple

FILEPATH = str(Path(__file__).parent / 'input.txt')

class Game:
    def __init__(self, index, draws):
        self.index = index
        self.draws = draws
    
    def check_possible(self, red, green, blue):
        # If any of the draws exceed the provided amount of colors, then it is not possible
        for draw in self.draws:
            if ('red' in draw and draw['red'] > red) or ('green' in draw and draw['green'] > green) or ('blue' in draw and draw['blue'] > blue):
                return False
        return True

    # Power is the product of the minimum amount of red, blue and green colors needed
    def get_power(self):
        red = 0
        green = 0
        blue = 0
        for draw in self.draws:
            if 'red' in draw:
                red = max(red, draw['red'])
            if 'green' in draw:
                green = max(green, draw['green'])
            if 'blue' in draw:
                blue = max(blue, draw['blue'])
        
        return red * green * blue

def parse_line(line: str) -> Game:
    game, sets = line.split(':')
    index = int(game.split(' ')[1])
    total_draws = []
    for draw in sets.split(';'):
        draw_dict = {}
        for combi in draw.split(', '):
            combi = combi.strip().rstrip()
            num, color = combi.split(' ')
            draw_dict[color] = int(num)
        total_draws.append(draw_dict)
    return Game(index, total_draws)


def load_txt(filepath) -> list[int]:
    games = []
    with open(filepath, mode='r') as file:
        for line in file.readlines():
            games.append(parse_line(line))
    return games


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--filepath', type=lambda path: str(Path(path).absolute()), default=FILEPATH)
    pargs = parser.parse_args()
    # part 1
    games = load_txt(pargs.filepath)
    score = 0
    for game in games:
        if game.check_possible(12, 13, 14):
            score += game.index
    print(f"Result for part 1: {score}")
    # part 2
    print(f"Result for part 2: {sum(game.get_power() for game in games)}")
