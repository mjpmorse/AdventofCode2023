from src.day04.day04 import part1, part2


def test_part1():
    part1_solution = part1("data/day04/input_sample.txt")
    assert part1_solution == 13


def test_part2():
    part1_solution = part2("data/day04/input_sample.txt")
    assert part1_solution == 30