import intcode
import inputreader
import day2


def part1(input):
    mem = day2.process_input(input)
    data, outs = intcode.compute(mem, [1])
    return outs


if __name__ == "__main__":
    input = inputreader.read("day5.txt")
    print(part1(input))
