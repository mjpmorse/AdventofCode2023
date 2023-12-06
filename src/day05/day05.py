from collections import OrderedDict
from dataclasses import dataclass, field
from typing import List, Dict
from copy import deepcopy
from icecream import ic

@dataclass
class IslandIslandAlmanac:
    initial_seeds: List[int]
    true_initial: List[range]
    seed_to_soil_dict: Dict[range, range] = field(default_factory=lambda: {})
    soil_to_fertilizer_dict: Dict[range, range] = field(default_factory=lambda: {})
    fertilizer_to_water_dict: Dict[range, range] = field(default_factory=lambda: {})
    water_to_light_dict: Dict[range, range] = field(default_factory=lambda: {})
    light_to_temperature_dict: Dict[range, range] = field(default_factory=lambda: {})
    temperature_to_humidity_dict: Dict[range, range] = field(default_factory=lambda: {})
    humidity_to_location_dict: Dict[range, range] = field(default_factory=lambda: {})

    @staticmethod
    def _find_distance(lookup_dict: dict, nbr: int):
        for key, value in lookup_dict.items():
            if nbr in key:
                dist = nbr - key.start
                target_value = value.start + dist
                return target_value
        return nbr

    def seed_to_soil(self, nbr: int):
        return self._find_distance(self.seed_to_soil_dict, nbr)

    def soil_to_fertilizer(self, nbr: int):
        return self._find_distance(self.soil_to_fertilizer_dict, nbr)

    def fertilizer_to_water(self, nbr: int):
        return self._find_distance(self.fertilizer_to_water_dict, nbr)

    def water_to_light(self, nbr: int):
        return self._find_distance(self.water_to_light_dict, nbr)

    def light_to_temperature(self, nbr: int):
        return self._find_distance(self.light_to_temperature_dict, nbr)

    def temperature_to_humidity(self, nbr: int):
        return self._find_distance(self.temperature_to_humidity_dict, nbr)

    def humidity_to_location(self, nbr: int):
        return self._find_distance(self.humidity_to_location_dict, nbr)

    def seed_to_location(self, starting_seed: int):
        soil = self.seed_to_soil(starting_seed)
        fertilizer = self.soil_to_fertilizer(soil)
        water = self.fertilizer_to_water(fertilizer)
        light = self.water_to_light(water)
        temp = self.light_to_temperature(light)
        humidity = self.temperature_to_humidity(temp)
        location = self.humidity_to_location(humidity)
        return location

    def location_to_seed(self, starting_location):
        humidity = self._find_distance({v: k for k, v in self.humidity_to_location_dict.items()}, starting_location)
        temp = self._find_distance({v: k for k, v in self.temperature_to_humidity_dict.items()}, humidity)
        light = self._find_distance({v: k for k, v in self.light_to_temperature_dict.items()}, temp)
        water = self._find_distance({v: k for k, v in self.water_to_light_dict.items()}, light)
        fertilizer = self._find_distance({v: k for k, v in self.fertilizer_to_water_dict.items()}, water)
        soil = self._find_distance({v: k for k, v in self.soil_to_fertilizer_dict.items()}, fertilizer)
        seed = self._find_distance({v: k for k, v in self.seed_to_soil_dict.items()}, soil)
        return seed

    @property
    def min_possible_value(self):
        return min([
            min([x.start for x in self.humidity_to_location_dict.keys()]),
            min([x.start for x in self.humidity_to_location_dict.values()]),
            min([x.start for x in self.temperature_to_humidity_dict.keys()]),
            min([x.start for x in self.temperature_to_humidity_dict.values()]),
            min([x.start for x in self.light_to_temperature_dict.keys()]),
            min([x.start for x in self.light_to_temperature_dict.values()]),
            min([x.start for x in self.water_to_light_dict.keys()]),
            min([x.start for x in self.water_to_light_dict.values()]),
            min([x.start for x in self.fertilizer_to_water_dict.keys()]),
            min([x.start for x in self.fertilizer_to_water_dict.values()]),
            min([x.start for x in self.soil_to_fertilizer_dict.keys()]),
            min([x.start for x in self.soil_to_fertilizer_dict.values()]),
            min([x.start for x in self.seed_to_soil_dict.keys()]),
            min([x.start for x in self.seed_to_soil_dict.values()]),
        ])

    def _check_guess(self, guess):
        for x in self.true_initial:
            if guess in x:
                return True
        return False

    def lowest_seed_finder(self):
        lowest_location = 0
        while True:
            seed_guess = self.location_to_seed(lowest_location)
            if self._check_guess(seed_guess):
                break
            lowest_location += 1
        return lowest_location
    @staticmethod
    def _check_range(test_range: range, compare_range: range) -> List[range]:
        """
        There are 5 possibilities
        1. the test range does not over lap the compare range (1 range returned)
        2. the test range overlaps to the left (2 ranges returned)
        3. the test range overlaps to the right (2 ranges returned)
        4. the test range covers the compare range (3 ranges returned)
        5. the test range is less than or equal to compare range (1 range returned)
        :param test_range: the test range
        :param compare_range: the range to compare it to
        :return:
        """
        # TODO: FIX THIS
        left_test = test_range.start
        right_test = test_range[-1]
        left_compare = compare_range.start
        right_compare = compare_range[-1]

        # condition 2
        if (
                (left_test < left_compare) &
                (right_test > right_compare) &
                (right_test < right_compare)
        ):
            return [range(left_test, left_compare), range(right_compare, right_test + 1)]
        # condition 3
        if (
                (left_test > left_compare) &
                (left_test < right_compare) &
                (right_test > right_compare)
        ):
            return [range(left_test, right_compare + 1), range(right_compare + 1, right_test + 1)]
        # condition 4
        if (
                (left_test < left_compare) &
                (right_test > right_compare)
        ):
            return [
                range(left_test, left_compare),
                range(left_compare, right_compare + 1),
                range(right_compare + 1, right_test + 1)
            ]
        # condition 5
        if (
                (left_test >= left_compare) &
                (right_test <= right_compare)
        ):
            return [test_range]
        # condition 1 is all else
        return [test_range]

    def _split_ranges(
            self, test_ranges: List[range], compare_ranges: List[range]
    ) -> List[range]:
        # TODO: FIX THIS
        while True:
            test_ranges = deepcopy(test_ranges)
            initial_length = len(test_ranges)
            for idx in range(0, initial_length):
                test_range = test_ranges.pop(0)
                for compare_range in compare_ranges:
                    new_ranges = self._check_range(test_range, compare_range)
                    test_ranges.extend(new_ranges)
                    test_ranges = list(set(test_ranges))
            final_length = len(test_ranges)
            if final_length == initial_length:
                break
            if final_length < initial_length:
                pass
            if final_length > 20:
                ic(test_ranges)
                raise Exception
        ic(test_ranges)
        return test_ranges

    @staticmethod
    def _convert_ranges(
            initial_ranges: List[range], range_dict: Dict[range, range]
    ) -> List[range]:
        return_list = []
        ic(initial_ranges)
        ic(range_dict)
        for _range in initial_ranges:
            for key, value in range_dict.items():
                if (
                        (_range.start >= key.start) &
                        (_range[-1] <= key[-1])
                ):
                    distance_in = _range.start - key.start
                    total_distance = len(_range)
                    return_start = value.start + distance_in
                    return_end = return_start + total_distance
                    return_list.append(range(return_start, return_end))
                else:
                    return_list.append(_range)
        return return_list

    def _split_and_convert(
            self, test_ranges: List[range], range_dict: Dict[range, range]
    ) -> List[range]:
        compare_ranges = list(range_dict.keys())
        ic(compare_ranges)
        split_ranges = self._split_ranges(test_ranges, compare_ranges)
        ic(split_ranges)
        return self._convert_ranges(split_ranges, range_dict)

    def initial_seed_ranges_to_loc(self):
        soil = self._split_and_convert(self.true_initial, self.seed_to_soil_dict)
        fertilizer = self._split_and_convert(soil, self.soil_to_fertilizer_dict)
        water = self._split_and_convert(fertilizer, self.fertilizer_to_water_dict)
        light = self._split_and_convert(water, self.water_to_light_dict)
        temp = self._split_and_convert(light, self.light_to_temperature_dict)
        humidity = self._split_and_convert(temp, self.temperature_to_humidity_dict)
        location = self._split_and_convert(humidity, self.humidity_to_location_dict)
        return location

    @property
    def initial_seed_locations(self):
        return_list = []
        for seed in self.initial_seeds:
            return_list.append(self.seed_to_location(seed))
        return return_list


def parse_almanac_file(path) -> IslandIslandAlmanac:
    parsing_dict = OrderedDict({
        'seed-to-soil map:': {},
        'soil-to-fertilizer map:': {},
        'fertilizer-to-water map:': {},
        'water-to-light map:': {},
        'light-to-temperature map:': {},
        'temperature-to-humidity map:': {},
        'humidity-to-location map:': {}
    })
    keys = list(parsing_dict.keys())
    with open(f'{path}', 'r') as f:
        dict_element = -1
        for line in f:
            line = line.strip()
            if 'seeds: ' in line:
                line = line.split('seeds:')[1]
                line = line.strip()
                initial_seeds = [int(x) for x in line.split(" ") if x != ""]
                starting_seeds = initial_seeds[::2]
                starting_ranges = initial_seeds[1::2]
                true_initial = []
                for seed, _range in zip(starting_seeds, starting_ranges):
                    true_initial.append(range(seed, seed + _range))
                continue
            if line == '':
                continue
            if '-to-' in line:
                dict_element = dict_element + 1
                continue
            else:
                destination, source, length = [int(x) for x in line.split()]
                key = range(source, source + length)
                value = range(destination, destination + length)
                parsing_dict[keys[dict_element]][key] = value
    return IslandIslandAlmanac(
        initial_seeds=initial_seeds,
        true_initial=true_initial,
        seed_to_soil_dict=parsing_dict['seed-to-soil map:'],
        soil_to_fertilizer_dict=parsing_dict['soil-to-fertilizer map:'],
        fertilizer_to_water_dict=parsing_dict['fertilizer-to-water map:'],
        water_to_light_dict=parsing_dict['water-to-light map:'],
        light_to_temperature_dict=parsing_dict['light-to-temperature map:'],
        temperature_to_humidity_dict=parsing_dict['temperature-to-humidity map:'],
        humidity_to_location_dict=parsing_dict['humidity-to-location map:'],
    )


def part1(path):
    almanac = parse_almanac_file(path)
    starting_locations = almanac.initial_seed_locations
    return min(starting_locations)


def part2(path):
    almanac = parse_almanac_file(path)
    lowest_location = almanac.lowest_seed_finder()
    # locations = almanac.initial_seed_ranges_to_loc()
    return lowest_location



if __name__ == '__main__':
    part1_solution = part1('data/day05/input.txt')
    print(f'The lowest location number that corresponds to any of the initial seed numbers is {part1_solution}')

    part2_solution = part2('data/day05/input.txt')
    print(f'The lowest location number that corresponds to any of the initial seed numbers is {part2_solution}')
