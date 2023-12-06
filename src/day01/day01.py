from typing import List, Iterable, Tuple, Union
from dataclasses import dataclass
from copy import deepcopy


def read_calibration_document(path: str) -> List[str]:
    calibration_document = []
    with open(f'{path}', 'r') as f:
        for line in f:
            calibration_document.append(line)

    return calibration_document


@dataclass
class ElfInteger:
    position: int
    integer: int


def find_first_int(x: Iterable) -> Union[ElfInteger, None]:
    # python 3.11 has zero cost exception handling
    for idx, z in enumerate(x):
        try:
            nbr = int(z)
            return ElfInteger(position=idx, integer=nbr)
        except ValueError:
            continue
    return None


def find_list(x: str, check_list: list) -> Tuple[Union[ElfInteger, None], Union[ElfInteger, None]]:
    # we want to know if any of spellings are substrings of x
    position_number_dir = {}
    for nbr in check_list:
        x_new = deepcopy(x)
        while x_new.find(nbr) != -1:
            position_number_dir[x_new.find(nbr)] = nbr
            x_new = x_new.replace(nbr, "#" * len(nbr), 1)

    if len(position_number_dir) < 1:
        return None, None
    # now get the lowest key value
    lowest_position = min(position_number_dir.keys())
    lowest_nbr = check_list.index(position_number_dir[lowest_position]) + 1
    # now get the highest key value
    highest_position = max(position_number_dir.keys())
    highest_nbr = check_list.index(position_number_dir[highest_position]) + 1

    return (
        ElfInteger(position=lowest_position, integer=lowest_nbr),
        ElfInteger(position=highest_position, integer=highest_nbr)
    )


def part1(path: str) -> int:
    number_list = []
    calibration_document = read_calibration_document(path)
    for line in calibration_document:
        nbrs = [str(x) for x in [1, 2, 3, 4, 5, 6, 7, 8, 9]]
        first_int, last_int = find_list(line, nbrs)
        number_list.append(int(f"{first_int.integer}{last_int.integer}"))
    return sum(number_list)


def part2(path: str) -> int:
    number_list = []
    calibration_document = read_calibration_document(path)
    spellings = [
        'one', 'two', 'three', 'four', 'five',
        'six', 'seven', 'eight', 'nine'
    ]
    nbrs = [str(x) for x in [1, 2, 3, 4, 5, 6, 7, 8, 9]]

    for line in calibration_document:
        first_int = None
        last_int = None
        first_potential_int, last_potential_int = find_list(line, nbrs)
        first_potential_spelled_int, last_potential_spelled_int = find_list(line.lower(), spellings)

        # if the first is None and last will also be None
        if first_potential_spelled_int is None:
            first_int = first_potential_int.integer
            last_int = last_potential_int.integer
            number_list.append(int(f"{first_int}{last_int}"))
            continue

        if first_potential_int is None:
            first_int = first_potential_spelled_int.integer
            last_int = last_potential_spelled_int.integer
            number_list.append(int(f"{first_int}{last_int}"))
            continue

        if first_potential_int.position < first_potential_spelled_int.position:
            first_int = first_potential_int.integer
        elif first_potential_int.position > first_potential_spelled_int.position:
            first_int = first_potential_spelled_int.integer
        else:
            raise Exception('This should not happen')

        if last_potential_int.position > last_potential_spelled_int.position:
            last_int = last_potential_int.integer
        elif last_potential_int.position < last_potential_spelled_int.position:
            last_int = last_potential_spelled_int.integer
        else:
            raise Exception('This should not happen')
        number_list.append(int(f"{first_int}{last_int}"))
    return sum(number_list)


if __name__ == '__main__':
    part1_answer = part1('./data/day01/part1.txt')
    print(f'The part 1 solution is {part1_answer}')

    part2_answer = part2('./data/day01/part2.txt')
    print(f'The part 2 solution is {part2_answer}')