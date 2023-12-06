from collections import OrderedDict
from dataclasses import dataclass, field
from typing import List, Dict
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
    return lowest_location


if __name__ == '__main__':
    part1_solution = part1('data/day05/input.txt')
    print(f'The lowest location number that corresponds to any of the initial seed numbers is {part1_solution}')

    part2_solution = part2('data/day05/input.txt')
    print(f'The lowest location number that corresponds to any of the initial seed numbers is {part2_solution}')
