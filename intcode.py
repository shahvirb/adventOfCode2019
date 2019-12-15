import typing


class State:
    I_STEP = 1

    def __init__(
        self, data: typing.List, i: int = 0, read_modes=None, inputs=None, outputs=None
    ):
        self.data = data
        self.i = i
        assert i <= len(data)
        self.read_modes = read_modes
        self.inputs = inputs
        self.outputs = outputs

    def do(self):
        pass

    def next_state(self):
        assert self.i + self.I_STEP <= len(self.data)
        return ExecState(
            self.data, self.i + self.I_STEP, inputs=self.inputs, outputs=self.outputs
        )

    def __repr__(self):
        return ",".join([str(d) for d in self.data[self.i : self.i + self.I_STEP]])


def read_mem(mem, i, mode):
    """
    >>> read_mem([1,2,3], 0, 0)
    2
    >>> read_mem([1,2,3], 2, 1)
    3
    """
    assert mode == 0 or mode == 1
    return mem[i if mode == 1 else mem[i]]


def read_params(data, i, modes, count=2):
    return [
        read_mem(data, i + 1 + n, modes[n] if n < len(modes) else 0,)
        for n in range(0, count)
    ]


class AddState(State):
    I_STEP = 4

    def do(self):
        params = read_params(self.data, self.i, self.read_modes)
        self.data[self.data[self.i + 3]] = sum(params)


class MultState(State):
    I_STEP = 4

    def do(self):
        params = read_params(self.data, self.i, self.read_modes)
        self.data[self.data[self.i + 3]] = params[0] * params[1]


class InputState(State):
    I_STEP = 2

    def do(self):
        assert self.inputs
        self.data[self.data[self.i + 1]] = self.inputs.pop(0)


class OutputState(State):
    I_STEP = 2

    def do(self):
        assert self.outputs is not None
        params = read_params(self.data, self.i, self.read_modes, 1)
        self.outputs.append(params[0])


class JumpTrueState(State):
    I_STEP = 3

    def do(self):
        params = read_params(self.data, self.i, self.read_modes)
        if params[0] != 0:
            self.i = (
                params[1] - self.I_STEP
            )  # subtract I_STEP because super class will add I_STEP


class JumpFalseState(State):
    I_STEP = 3

    def do(self):
        params = read_params(self.data, self.i, self.read_modes)
        if params[0] == 0:
            self.i = (
                params[1] - self.I_STEP
            )  # subtract I_STEP because super class will add I_STEP


class CmpLessState(State):
    I_STEP = 4

    def do(self):
        params = read_params(self.data, self.i, self.read_modes, 2)
        self.data[self.data[self.i + 3]] = 1 if params[0] < params[1] else 0


class CmpEqualsState(State):
    I_STEP = 4

    def do(self):
        params = read_params(self.data, self.i, self.read_modes, 2)
        self.data[self.data[self.i + 3]] = 1 if params[0] == params[1] else 0


def parse_code(code):
    """
    >>> parse_code(2)
    (2, ())
    >>> parse_code(3)
    (3, ())
    >>> parse_code(1002)
    (2, (0, 1))
    >>> parse_code(11003)
    (3, (0, 1, 1))
    """
    cstr = str(code)
    return int(cstr[-2:]), tuple(int(c) for c in reversed(cstr[:-2]))


class ExecState(State):
    def next_state(self):
        COMMAND_MAP = {
            1: AddState,
            2: MultState,
            3: InputState,
            4: OutputState,
            5: JumpTrueState,
            6: JumpFalseState,
            7: CmpLessState,
            8: CmpEqualsState,
            99: None,
        }
        cmd, modes = parse_code(self.data[self.i])
        state = COMMAND_MAP[cmd]
        return (
            state(self.data, self.i, modes, self.inputs, self.outputs)
            if state
            else None
        )


class Computer:
    def __init__(self, mem, inputs=None, run=True):
        self.mem = mem.copy()
        self.inputs = inputs
        self.outputs = []
        if run:
            self.run()

    def run(self):
        curr = ExecState(self.mem, 0, inputs=self.inputs, outputs=self.outputs)
        while curr:
            curr.do()
            curr = curr.next_state()


def compute(mem, inputs=None):
    """
    >>> compute([1001,0,0,3,99])
    ([1001, 0, 0, 1001, 99], [])
    >>> compute([1002,0,3,3,99])
    ([1002, 0, 3, 3006, 99], [])
    >>> compute([3, 1, 99], [-5])
    ([3, -5, 99], [])
    >>> compute([3, 1, 3, 2, 99], [-5, -6])
    ([3, -5, -6, 2, 99], [])
    >>> compute([4,0,99])
    ([4, 0, 99], [4])
    >>> compute([104,86,99])
    ([104, 86, 99], [86])
    >>> compute([1105, 0, 300, 99])
    ([1105, 0, 300, 99], [])
    >>> compute([1105, 13, 6, -1, -1, -1, 99])
    ([1105, 13, 6, -1, -1, -1, 99], [])
    >>> compute([1106, 13, 300, 99])
    ([1106, 13, 300, 99], [])
    >>> compute([1108,1,1,5,99,-1])
    ([1108, 1, 1, 5, 99, 1], [])
    >>> compute([108,-1,5,6,99,-1, -1])
    ([108, -1, 5, 6, 99, -1, 1], [])
    >>> compute([1107,1,2,5,99,-1])
    ([1107, 1, 2, 5, 99, 1], [])
    >>> compute([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], [0])
    ([3, 3, 1105, 0, 9, 1101, 0, 0, 12, 4, 12, 99, 0], [0])
    """
    c = Computer(mem, inputs)
    return c.mem, c.outputs


if __name__ == "__main__":
    import doctest

    doctest.testmod()
