import typing


class State:
    I_STEP = 1

    def __init__(self, data: typing.List, i: int = 0, read_modes=None, inputs=None):
        self.data = data
        self.i = i
        assert i <= len(data)
        self.read_modes = read_modes
        self.inputs = inputs

    def do(self):
        pass

    def next_state(self):
        assert self.i + self.I_STEP <= len(self.data)
        return ExecState(self.data, self.i + self.I_STEP, inputs=self.inputs)


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


class InputState(State):
    I_STEP = 2

    def do(self):
        assert self.inputs
        self.data[self.data[self.i + 1]] = self.inputs.pop(0)


COMMAND_MAP = {1: AddState, 2: MultState, 3: InputState, 99: None}


def parse_code(code):
    """
    >>> parse_code(1002)
    (2, (0, 1))
    >>> parse_code(11003)
    (3, (0, 1, 1))
    >>> parse_code(3)
    (3, ())
    """
    if code in (3, 4, 99):
        return code, ()
    cstr = str(code)
    return int(cstr[-2:]), tuple(int(c) for c in reversed(cstr[:-2]))


class ExecState(State):
    def next_state(self):
        cmd, modes = parse_code(self.data[self.i])
        state = COMMAND_MAP[cmd]
        return state(self.data, self.i, modes, self.inputs) if state else None


def compute(mem, inputs=None):
    """
    >>> compute([1001,0,0,3,99])
    [1001, 0, 0, 1001, 99]
    >>> compute([1002,0,3,3,99])
    [1002, 0, 3, 3006, 99]
    >>> compute([3, 1, 99], [-5])
    [3, -5, 99]
    >>> compute([3, 1, 3, 2, 99], [-5, -6])
    [3, -5, -6, 2, 99]
    """
    data = mem.copy()
    curr = ExecState(data, 0, inputs=inputs)
    while curr:
        curr.do()
        curr = curr.next_state()
    return data


if __name__ == "__main__":
    import doctest

    doctest.testmod()
