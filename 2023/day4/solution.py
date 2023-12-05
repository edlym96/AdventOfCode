from functools import cached_property
from pathlib import Path

FILEPATH = str(Path(__file__).parent / 'input.txt')

class Card:
    def __init__(self, index, winning_numbers: set[int], avail_numbers: set[int]):
        self.index = index
        self.winning = winning_numbers
        self.available = avail_numbers
    
    # Part 1 score
    def get_score(self):
        won = len(self.available & self.winning)
        if won == 0:
            return 0
        return 2**(won - 1)

    @cached_property
    def won_cards(self):
        won = len(self.available & self.winning)
        return [self.index + i for i in range(1, won+1)]

def load_txt() -> list[Card]:
    cards = {}
    with open(FILEPATH, mode='r') as file:
        for line in file.readlines():
            first, second = line.split('|')
            # filter out "Card"
            first = first[4:]
            # Filter out leading and trailing whitespace
            first = first.strip().rstrip()
            first_elems = first.split(' ')
            idx = int(first_elems[0].strip()[:-1])
            winning_nums = set([int(num) for num in first_elems[1:] if len(num)])
            second = second.strip().rstrip()
            available_nums = set([int(num) for num in second.split(' ') if len(num)])
            cards[idx] = Card(idx, winning_nums, available_nums)
    return cards
            

if __name__ == "__main__":
    
    # part 1
    cards = load_txt()
    print(f"Score for part 1: {sum(card.get_score() for card in cards.values())}")
    # print(f"Min location for part 1: {min(locations)}")

    # part 2 (probably need to dfs this)
    card_count = len(cards)
    card_indices = list(range(1, len(cards)+1))

    results = {}
    def dfs(index):
        # If already got the result for this card, return
        if index in results:
            return results[index]
        # If card index greater than cards we have, return 0
        if index > card_count:
            return 0
        # count starts at 1, the card itself
        count = 1
        # Get the won indices and dfs through until leaf
        won_indices = cards[index].won_cards
        for card_idx in won_indices:
            count += dfs(card_idx)
        # Add the index to the results
        results[index] = count
        return count

    print(f"Score for part 2: {sum(dfs(i) for i in card_indices)}")
