import intcode
import inputreader


def part1(input):
    data = inputreader.to_intcode(input)
    c = intcode.Computer(data, [1])
    assert len(c.outputs) == 1
    return c.outputs[-1]


if __name__ == "__main__":
    input = inputreader.read("day9.txt")
    print(part1(input))
