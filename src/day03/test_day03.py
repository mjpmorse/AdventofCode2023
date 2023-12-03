from src.day03.day03 import part1, part2


def test_part1():
    solution = part1('data/day03/part1_sample.txt')
    assert solution == 4361


def test_part2():
    solution = part2('data/day03/part1_sample.txt')
    assert solution == 467835
