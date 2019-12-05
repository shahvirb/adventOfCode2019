import inputreader
import typing


class State:
    def __init__(self, data: typing.List, i: int = 0):
        self.data = data
        self.i = i
        assert i <= len(data)

    def do(self):
        pass

    def next_state(self):
        assert self.i + 4 <= len(self.data)
        return ExecState(self.data, self.i + 4)


class AddState(State):
    def do(self):
        self.data[self.data[self.i + 3]] = (
            self.data[self.data[self.i + 1]] + self.data[self.data[self.i + 2]]
        )


class MultState(State):
    def do(self):
        self.data[self.data[self.i + 3]] = (
            self.data[self.data[self.i + 1]] * self.data[self.data[self.i + 2]]
        )


COMMAND_MAP = {1: AddState, 2: MultState, 99: None}


class ExecState(State):
    def next_state(self):
        state = COMMAND_MAP[self.data[self.i]]
        return state(self.data, self.i) if state else None


def compute(input, n, v):
    data = input.copy()
    data[1] = n
    data[2] = v
    curr = ExecState(data, 0)
    while curr:
        curr.do()
        curr = curr.next_state()
    return data


def find(input, search):
    for noun in range(99):
        for verb in range(99):
            data = compute(input, noun, verb)
            if data[0] == search:
                return noun, verb


def process_input(input):
    return [int(s) for s in input.split(",")]


def part1(input):
    return compute(process_input(input), 12, 2)[0]


def part2(input):
    n, v = find(process_input(input), 19690720)
    return 100 * n + v


if __name__ == "__main__":
    input = inputreader.read("day2.txt")

    print(part1(input))
    print(part2(input))
