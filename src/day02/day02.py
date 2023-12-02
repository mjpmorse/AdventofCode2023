from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class ElfGame:
    game_id: int
    red_list: List[int] = field(default_factory=lambda: [])
    green_list: List[int] = field(default_factory=lambda: [])
    blue_list: List[int] = field(default_factory=lambda: [])

    @property
    def nbr_of_round(self):
        return len(self.red_list)

    def add_round(self, red: int, green: int, blue: int):
        self.red_list.append(red)
        self.blue_list.append(blue)
        self.green_list.append(green)

    def is_possible(self, red, green, blue) -> bool:
        if (
                (max(self.red_list) > red) or
                (max(self.green_list) > green) or
                (max(self.blue_list) > blue)
        ):
            return False
        else:
            return True

    @property
    def minimum_cubes(self) -> Dict[str, int]:
        min_red = max(self.red_list)
        min_blue = max(self.blue_list)
        min_green = max(self.green_list)
        return {"red": min_red, 'blue': min_blue, "green": min_green}


def read_game_record(path: str) -> List[ElfGame]:
    elf_games = []
    with open(f'{path}', 'r') as f:
        for line in f:
            game_idx, game_rounds = line.split(":")
            # extract the game index
            game_idx = int(game_idx.split("Game ")[1])
            game_rounds = game_rounds.split(';')
            elf_game = ElfGame(game_idx)
            for game_round in game_rounds:
                split_round = game_round.split(",")
                nbr_red = 0
                nbr_blue = 0
                nbr_green = 0
                for grp in split_round:
                    if 'red' in grp:
                        tmp: str = grp.replace('red', '')
                        nbr_red = int(tmp.strip())
                        continue
                    if 'green' in grp:
                        tmp: str = grp.replace('green', '')
                        nbr_green = int(tmp.strip())
                        continue
                    if 'blue' in grp:
                        tmp: str = grp.replace('blue', '')
                        nbr_blue = int(tmp.strip())
                        continue
                elf_game.add_round(red=nbr_red, blue=nbr_blue, green=nbr_green)
            elf_games.append(elf_game)
    return elf_games


def part1(path: str, red: int, green: int, blue: int) -> int:
    game_list = read_game_record(path)
    sum_of_possible = 0
    for game in game_list:
        possible = game.is_possible(red=red, green=green, blue=blue)
        if possible:
            sum_of_possible += game.game_id
    return sum_of_possible


def part2(path: str) -> int:
    game_list = read_game_record(path)
    power_list = []
    for game in game_list:
        local_power = 1
        minimal_cubes = game.minimum_cubes
        for value in minimal_cubes.values():
            local_power *= value
        power_list.append(local_power)
    return sum(power_list)


if __name__ == '__main__':
    total = part1(
        'data/day02/part1.txt',
        red=12, green=13, blue=14
    )
    print(f'The sum of the IDs is: {total}')

    total = part2(
        'data/day02/part1.txt',
    )
    print(f'The sum of the power of these sets is: {total}')
