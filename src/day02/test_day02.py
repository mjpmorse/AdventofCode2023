from src.day02.day02 import part1, part2


def test_part1():
    red = 12
    green = 13
    blue = 14
    total = part1(
        'data/day02/part1_sample.txt',
        red=red, green=green, blue=blue
    )
    assert total == 8


def test_part2():

    total = part2(
        'data/day02/part1_sample.txt',
    )
    assert total == 2286
