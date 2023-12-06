from src.day05.day05 import part1, part2


def test_part1():
    result = part1('data/day05/input_sample.txt')
    assert result == 35


def test_part2():
    result = part2('data/day05/input_sample.txt')
    assert result == 46
