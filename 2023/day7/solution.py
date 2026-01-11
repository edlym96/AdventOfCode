#!/usr/bin/env python3
import argparse
import enum
from pathlib import Path
from collections import namedtuple, Counter
import functools

FILEPATH = str(Path(__file__).parent / 'input.txt')

# Used when comparing individual cards. Larger is stronger
CARD_POWER = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'T': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14,
}

# J is now Joker, weakest card
CARD_POWER_PART2 = {
    'J': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'T': 10,
    'Q': 12,
    'K': 13,
    'A': 14,
}

@functools.total_ordering
class HandType(enum.Enum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    TRIPLE = 4
    TWO_PAIR = 3
    PAIR = 2
    HIGH = 1

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
    
    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented

    @staticmethod
    def _card_count_to_type(count, card_dict):
        if count == 5:
            return HandType.FIVE_OF_A_KIND
        elif count == 4:
            return HandType.FOUR_OF_A_KIND
        elif count == 3:
            _, next_count = card_dict.popitem()
            if next_count == 2:
                return HandType.FULL_HOUSE
            else:
                return HandType.TRIPLE
        elif count == 2:
            _, next_count = card_dict.popitem()
            if next_count == 2:
                return HandType.TWO_PAIR
            else:
                return HandType.PAIR
        else:
            return HandType.HIGH
    
    @classmethod
    def from_cards(cls, cards):
        card_dict = Counter(cards)
        card_dict = dict(sorted(card_dict.items(), key=lambda item: item[1]))
        _, count = card_dict.popitem()
        return cls._card_count_to_type(count, card_dict)
    
    @classmethod
    def from_cards_part2(cls, cards):
        card_dict = Counter(cards)
        card_dict = dict(sorted(card_dict.items(), key=lambda item: item[1]))
        # Get all jokers
        if 'J' in card_dict:
            j_count = card_dict.pop('J')
        else:
            j_count = 0
        try:
            _, count = card_dict.popitem()
        except KeyError:
            # All were Jokers
            assert j_count == 5
            count = 0
        count += j_count
        return cls._card_count_to_type(count, card_dict)
    

@functools.total_ordering
class Hand:
    def __init__(self, cards, bid):
        self.cards = cards
        self.bid = bid
        self.hand_type = HandType.from_cards(cards)
        self.power_dict = CARD_POWER

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            # If hand types are the same, compare individual cards in order
            if self.hand_type == other.hand_type:
                for s_card, o_card in zip(self.cards, other.cards):
                    s_power = self.power_dict[s_card] 
                    o_power = self.power_dict[o_card]
                    if s_power == o_power:
                        continue
                    return s_power < o_power
            return self.hand_type < other.hand_type
        return NotImplemented
    
    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.cards == other.cards and self.bid == other.bid
        return NotImplemented

    # Part 2 has joker. Could also inherit Hand class, but this is more convenient to patch in
    def convert_to_part2(self):
        self.hand_type = HandType.from_cards_part2(self.cards)
        self.power_dict = CARD_POWER_PART2

def load_txt(filepath) -> list[Hand]:
    hands = []
    with open(filepath, mode='r') as file:
        for line in file.readlines():
            cards, bid = line.split(" ")
            hands.append(Hand(cards, int(bid)))
    return hands

def get_score(hands: list[Hand]):
    score = 0
    for multiplier, hand in enumerate(sorted(hands)):
        score += (multiplier + 1) * hand.bid
    return score

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--filepath', type=lambda path: str(Path(path).absolute()), default=FILEPATH)
    pargs = parser.parse_args()
    # part 1
    hands = load_txt(pargs.filepath)
    print(f"Result for part 1: {get_score(hands)}")
    # part 2
    # Convert hands to using new Joker card
    for hand in hands:
        hand.convert_to_part2()
    print(f"Result for part 2: {get_score(hands)}")
