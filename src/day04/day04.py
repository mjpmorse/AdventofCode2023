from collections import UserList
from copy import deepcopy
from dataclasses import dataclass, field
from typing import List, Union, Iterable, Dict

@dataclass
class ScratchCard:
    raw_card: str
    card_nbr: int
    winning_nbrs: List[int]
    test_nbrs: List[int]

    def card_value(self):
        nbr_matches = 0
        for nbr in self.test_nbrs:
            if nbr in self.winning_nbrs:
                nbr_matches += 1
        if nbr_matches == 0:
            return 0
        elif nbr_matches == 1:
            return 1
        else:
            return 2 ** (nbr_matches - 1)

    def cards_to_copy(self):
        nbr_matches = 0
        for nbr in self.test_nbrs:
            if nbr in self.winning_nbrs:
                nbr_matches += 1
        if nbr_matches == 0:
            return []
        else:
            return [self.card_nbr + x for x in range(1, nbr_matches + 1)]


class ScratchCardList(UserList):
    def __init__(self, iterable):
        super().__init__(item for item in iterable)
        self.card_frequency_dict: Dict[int, int] = {x.card_nbr: 1 for x in self.data}

    def find_card(self, card_nbr: int):
        for card in self.data:
            if card.card_nbr == card_nbr:
                return card
        raise Exception(f"Card # {card_nbr} was not found")

    def find_card_and_copy_n_times(self, card_nbr: Union[int, Iterable], n: int):
        if isinstance(card_nbr, int):
            card_nbr = [card_nbr]
        for nbr in card_nbr:
            self.card_frequency_dict[nbr] += n


def parse_input(path: str):
    card_list = []
    with open(f'{path}', 'r') as f:
        for line in f:
            # we are going to pad the rows
            line = line.strip()
            card_nbr, nbrs = line.split(":")
            card_nbr = int(card_nbr.split("Card ")[1])
            winning_nbrs, your_nbrs = nbrs.split("|")
            winning_nbrs = [int(x) for x in winning_nbrs.strip().split(" ") if x != ""]
            your_nbrs = [int(x) for x in your_nbrs.strip().split(" ") if x != ""]
            card = ScratchCard(line, card_nbr, winning_nbrs, your_nbrs)
            card_list.append(card)
        return card_list


def part1(path):
    card_list = parse_input(path)
    winnings = sum([x.card_value() for x in card_list])
    return winnings


def part2(path):
    card_list = ScratchCardList(parse_input(path))
    for card in card_list:
        card: ScratchCard
        nbr_of_copies = card_list.card_frequency_dict[card.card_nbr]
        cards_to_copy = card.cards_to_copy()
        card_list.find_card_and_copy_n_times(cards_to_copy, nbr_of_copies)
    return sum(card_list.card_frequency_dict.values())


if __name__ == '__main__':
    part1_solution = part1("data/day04/input.txt")
    print(f"There are {part1_solution} points in total")

    part2_solution = part2("data/day04/input.txt")
    print(f"You end up with {part2_solution} scratch cards")