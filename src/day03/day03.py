from copy import deepcopy
from dataclasses import dataclass, field
from typing import List


@dataclass
class EngineRow:
    row: str
    nbr_indexes: List[int] = field(default_factory=lambda: [])
    symbol_indexes: List[int] = field(default_factory=lambda: [])

    def find_and_remove_nbr(self, idx: int):
        """
        Finds the full number given the index of any part of it
        removes the full number from the nbr_index_list
        :param idx:
        :return:
        """
        if idx not in self.nbr_indexes:
            raise Exception("{idx} is not in the nbr index")
        # we now need to find all the continues indeces around the passed nbr
        # so if idx was 7 we need to know if 6, 5, 8, etc are in nbr_index
        lowest_index = idx
        highest_index = idx
        self.nbr_indexes.remove(idx)
        for idx_lwr in range(idx - 1, -1, -1):
            if idx_lwr in self.nbr_indexes:
                lowest_index = idx_lwr
                self.nbr_indexes.remove(idx_lwr)

            else:
                break
        for idx_upr in range(idx + 1, len(self.row)):
            if idx_upr in self.nbr_indexes:
                highest_index = idx_upr
                self.nbr_indexes.remove(idx_upr)
            else:
                break
        nbr = self.row[lowest_index: highest_index + 1]
        return int(nbr)


class Engine:
    def __init__(self, path):
        """
        :param path:
        :return:

        """
        engine_rows = []
        with open(f'{path}', 'r') as f:
            for line in f:
                # we are going to pad the rows
                line = line.strip()
                line = f".{line}."
                engine_line = EngineRow(row=line)
                for idx, _chr in enumerate(line):
                    try:
                        int(_chr)
                        engine_line.nbr_indexes.append(idx)
                        continue
                    except ValueError:
                        pass
                    if _chr != ".":
                        engine_line.symbol_indexes.append(idx)
                engine_rows.append(engine_line)

        # add padding on top and bottom
        first_last_row = '.' * len(line)
        first_row = EngineRow(row=first_last_row)
        last_row = EngineRow(row=first_last_row)
        engine_rows.insert(0, first_row)
        engine_rows.append(last_row)
        self.engine = engine_rows

    @property
    def engine_matrix(self):
        return [x.row for x in self.engine]

    def find_engine_parts(self):
        """
        For each row, iterate of the engine symbol list
        for each symbol check if there is a number around it
        if so, add the number to our part number list
        :return:
        """
        tmp_engine = deepcopy(self)
        part_nbr_list = []
        # now we iterate over the engine
        for idx_row in range(len(tmp_engine.engine)):
            #  we padded so fuck the first and last row special bullshit
            for idx_symbol in tmp_engine.engine[idx_row].symbol_indexes:
                #  check above and left
                if idx_symbol - 1 in tmp_engine.engine[idx_row - 1].nbr_indexes:
                    part_nbr = tmp_engine.engine[idx_row - 1].find_and_remove_nbr(idx_symbol - 1)
                    part_nbr_list.append(part_nbr)
                #  check above
                if idx_symbol in tmp_engine.engine[idx_row - 1].nbr_indexes:
                    part_nbr = tmp_engine.engine[idx_row - 1].find_and_remove_nbr(idx_symbol)
                    part_nbr_list.append(part_nbr)
                # check above and right
                if idx_symbol + 1 in tmp_engine.engine[idx_row - 1].nbr_indexes:
                    part_nbr = tmp_engine.engine[idx_row - 1].find_and_remove_nbr(idx_symbol + 1)
                    part_nbr_list.append(part_nbr)
                # check left
                if idx_symbol - 1 in tmp_engine.engine[idx_row].nbr_indexes:
                    part_nbr = tmp_engine.engine[idx_row].find_and_remove_nbr(idx_symbol - 1)
                    part_nbr_list.append(part_nbr)
                # check right
                if idx_symbol + 1 in tmp_engine.engine[idx_row].nbr_indexes:
                    part_nbr = tmp_engine.engine[idx_row].find_and_remove_nbr(idx_symbol + 1)
                    part_nbr_list.append(part_nbr)
                #  check below and left
                if idx_symbol - 1 in tmp_engine.engine[idx_row + 1].nbr_indexes:
                    part_nbr = tmp_engine.engine[idx_row + 1].find_and_remove_nbr(idx_symbol - 1)
                    part_nbr_list.append(part_nbr)
                #  check below
                if idx_symbol in tmp_engine.engine[idx_row + 1].nbr_indexes:
                    part_nbr = tmp_engine.engine[idx_row + 1].find_and_remove_nbr(idx_symbol)
                    part_nbr_list.append(part_nbr)
                # check below and right
                if idx_symbol + 1 in tmp_engine.engine[idx_row + 1].nbr_indexes:
                    part_nbr = tmp_engine.engine[idx_row + 1].find_and_remove_nbr(idx_symbol + 1)
                    part_nbr_list.append(part_nbr)
        return sum(part_nbr_list)

    def find_gear_ratio(self):
        """
        :return:
        """
        tmp_engine = deepcopy(self)
        gear_ratio_list = []
        # now we iterate over the engine
        for idx_row in range(len(tmp_engine.engine)):
            #  we padded so fuck the first and last row special bullshit
            for idx_symbol in tmp_engine.engine[idx_row].symbol_indexes:

                # only care about the multiply now
                if tmp_engine.engine[idx_row].row[idx_symbol] != '*':
                    continue

                gear_ratio = 1
                nbr_of_gears = 0
                #  check above and left
                if idx_symbol - 1 in tmp_engine.engine[idx_row - 1].nbr_indexes:
                    part_nbr = tmp_engine.engine[idx_row - 1].find_and_remove_nbr(idx_symbol - 1)
                    nbr_of_gears += 1
                    gear_ratio *= part_nbr
                #  check above
                if idx_symbol in tmp_engine.engine[idx_row - 1].nbr_indexes:
                    part_nbr = tmp_engine.engine[idx_row - 1].find_and_remove_nbr(idx_symbol)
                    nbr_of_gears += 1
                    gear_ratio *= part_nbr
                # check above and right
                if idx_symbol + 1 in tmp_engine.engine[idx_row - 1].nbr_indexes:
                    part_nbr = tmp_engine.engine[idx_row - 1].find_and_remove_nbr(idx_symbol + 1)
                    nbr_of_gears += 1
                    gear_ratio *= part_nbr
                # check left
                if idx_symbol - 1 in tmp_engine.engine[idx_row].nbr_indexes:
                    part_nbr = tmp_engine.engine[idx_row].find_and_remove_nbr(idx_symbol - 1)
                    nbr_of_gears += 1
                    gear_ratio *= part_nbr
                # check right
                if idx_symbol + 1 in tmp_engine.engine[idx_row].nbr_indexes:
                    part_nbr = tmp_engine.engine[idx_row].find_and_remove_nbr(idx_symbol + 1)
                    nbr_of_gears += 1
                    gear_ratio *= part_nbr
                #  check below and left
                if idx_symbol - 1 in tmp_engine.engine[idx_row + 1].nbr_indexes:
                    part_nbr = tmp_engine.engine[idx_row + 1].find_and_remove_nbr(idx_symbol - 1)
                    nbr_of_gears += 1
                    gear_ratio *= part_nbr
                #  check below
                if idx_symbol in tmp_engine.engine[idx_row + 1].nbr_indexes:
                    part_nbr = tmp_engine.engine[idx_row + 1].find_and_remove_nbr(idx_symbol)
                    nbr_of_gears += 1
                    gear_ratio *= part_nbr
                # check below and right
                if idx_symbol + 1 in tmp_engine.engine[idx_row + 1].nbr_indexes:
                    part_nbr = tmp_engine.engine[idx_row + 1].find_and_remove_nbr(idx_symbol + 1)
                    nbr_of_gears += 1
                    gear_ratio *= part_nbr

                if nbr_of_gears == 2:
                    gear_ratio_list.append(gear_ratio)

        return sum(gear_ratio_list)


def part1(path):
    part1_engine = Engine(path)
    solution = part1_engine.find_engine_parts()
    return solution


def part2(path):
    part1_engine = Engine(path)
    solution = part1_engine.find_gear_ratio()
    return solution


if __name__ == '__main__':
    part1_solution = part1('data/day03/part1.txt')
    print(f'The sum of all of the part numbers in the engine schematic is: {part1_solution}')
    part2_solution = part2('data/day03/part1.txt')
    print(f'The sum of all of the gear ratios in the engine schematic is: {part2_solution}')