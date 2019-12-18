import intcode
import inputreader


def solve(input, mode):
    data = inputreader.to_intcode(input)
    c = intcode.Computer(data, [mode])
    assert len(c.outputs) == 1
    return c.outputs[-1]


def part1(input):
    return solve(input, 1)


def part2(input):
    return solve(input, 2)


if __name__ == "__main__":
    input = inputreader.read("day9.txt")
    print(part1(input))
    print(part2(input))
