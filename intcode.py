import typing


class State:
    I_STEP = 1

    def __init__(self, data: typing.List, i: int = 0, read_modes=None):
        self.data = data
        self.i = i
        assert i <= len(data)
        if read_modes:
            self.read_modes = read_modes

    def do(self):
        pass

    def next_state(self):
        assert self.i + self.I_STEP <= len(self.data)
        # TODO this should be the step length of the instruction
        return ExecState(self.data, self.i + self.I_STEP)


def read_mem(mem, i, mode):
    """
    >>> read_mem([1,2,3], 0, 0)
    2
    >>> read_mem([1,2,3], 2, 1)
    3
    """
    assert mode == 0 or mode == 1
    return mem[i if mode == 1 else mem[i]]


def read_inputs(data, i, modes, count=2):
    return [
        read_mem(data, i + 1 + n, modes[n] if n < len(modes) else 0,)
        for n in range(0, count)
    ]


class AddState(State):
    I_STEP = 4

    def do(self):
        inputs = read_inputs(self.data, self.i, self.read_modes)
        self.data[self.data[self.i + 3]] = sum(inputs)


class MultState(State):
    I_STEP = 4

    def do(self):
        inputs = read_inputs(self.data, self.i, self.read_modes)
        self.data[self.data[self.i + 3]] = inputs[0] * inputs[1]


COMMAND_MAP = {1: AddState, 2: MultState, 99: None}


def parse_code(code):
    """
    >>> parse_code(1002)
    (2, (0, 1))
    >>> parse_code(11003)
    (3, (0, 1, 1))
    >>> parse_code(99)
    (99, ())
    """
    cstr = str(code)
    assert len(cstr) >= 2
    return int(cstr[-2:]), tuple(int(c) for c in reversed(cstr[:-2]))


class ExecState(State):
    def next_state(self):
        cmd, modes = parse_code(self.data[self.i])
        state = COMMAND_MAP[cmd]
        return state(self.data, self.i, modes) if state else None


def compute(input):
    """
    >>> compute([1001,0,0,3,99])
    [1001, 0, 0, 1001, 99]
    >>> compute([1002,0,3,3,99])
    [1002, 0, 3, 3006, 99]
    """
    data = input.copy()
    curr = ExecState(data, 0)
    while curr:
        curr.do()
        curr = curr.next_state()
    return data


if __name__ == "__main__":
    import doctest

    doctest.testmod()
