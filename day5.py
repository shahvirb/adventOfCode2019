import intcode
import inputreader
import day2


def part1(input):
    mem = inputreader.to_intcode(input)
    data, outs = intcode.compute(mem, [1])
    return outs


def part2(input):
    mem = inputreader.to_intcode(input)
    data, outs = intcode.compute(mem, [5])
    return outs


if __name__ == "__main__":
    input = inputreader.read("day5.txt")
    print(part1(input))
    print(part2(input))
