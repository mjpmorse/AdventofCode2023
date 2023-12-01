from src.day01.day01 import part1, read_calibration_document, part2


def test_part_1():
    part1_answer = part1('./data/day01/test_part1.txt')
    assert part1_answer == 142


def test_part_2():
    part1_answer = part2('./data/day01/test_part2.txt')
    assert part1_answer == 281