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


def compute(data):
    curr = ExecState(data, 0)
    while curr:
        curr.do()
        curr = curr.next_state()
    return data


if __name__ == "__main__":
    data = [int(s) for s in inputreader.readlines("day2.txt")[0].split(",")]
    # Part 1
    data[1] = 12
    data[2] = 2
    data = compute(data)
    print(data[0])
