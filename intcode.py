import enum
import typing
import pytest


class IntCodeNoInputError(Exception):
    def __str__(self):
        return "No input available"


class ParamMode(enum.Enum):
    POSITION = 0
    DIRECT = 1
    RELATIVE = 2


def address(mem, i, mode, rb=0):
    if mode == ParamMode.POSITION:
        return mem[i]
    if mode == ParamMode.DIRECT:
        return i
    if mode == ParamMode.RELATIVE:
        return mem[i] + rb


def test_address():
    def read_mem(mem, i, mode, rb=0):
        return mem[address(mem, i, mode, rb)]

    assert read_mem([1, 2, 3], 0, ParamMode.POSITION) == 2
    assert read_mem([1, 2, 3], 2, ParamMode.DIRECT) == 3
    assert read_mem([1, 2, 3], 2, ParamMode.RELATIVE, rb=-1) == 3
    assert read_mem([1, 2, 3, 4, 5], 1, ParamMode.RELATIVE, rb=2) == 5


def param_addresses(data, i, modes, count):
    return [
        address(data, i + 1 + n, modes[n] if n < len(modes) else ParamMode.POSITION)
        for n in range(0, count)
    ]


def test_param_addresses():
    assert param_addresses(
        [1001, 0, -13, 3, 99], 0, (ParamMode.POSITION, ParamMode.DIRECT), 3
    ) == [0, 2, 3]


class State:
    I_STEP = 1

    def __init__(self, computer, read_modes=()):
        self.computer = computer
        assert self.computer.i <= len(self.computer.data)
        self.read_modes = read_modes

    def do(self):
        pass

    def next_state(self):
        assert self.computer.i + self.I_STEP <= len(self.computer.data)
        self.computer.i += self.I_STEP
        return ExecState(self.computer)

    def __repr__(self):
        return ",".join(
            [
                str(d)
                for d in self.computer.data[
                    self.computer.i : self.computer.i + self.I_STEP
                ]
            ]
        )


class AddState(State):
    I_STEP = 4

    def do(self):
        addresses = param_addresses(
            self.computer.data, self.computer.i, self.read_modes, self.I_STEP - 1
        )
        self.computer.data[addresses[2]] = (
            self.computer.data[addresses[0]] + self.computer.data[addresses[1]]
        )


class MultState(State):
    I_STEP = 4

    def do(self):
        addresses = param_addresses(
            self.computer.data, self.computer.i, self.read_modes, self.I_STEP - 1
        )
        self.computer.data[addresses[2]] = (
            self.computer.data[addresses[0]] * self.computer.data[addresses[1]]
        )


class InputState(State):
    I_STEP = 2

    def do(self):
        if not self.computer.inputs:
            raise IntCodeNoInputError()
        addresses = param_addresses(
            self.computer.data, self.computer.i, self.read_modes, self.I_STEP - 1
        )
        self.computer.data[addresses[0]] = self.computer.inputs.pop(0)


class OutputState(State):
    I_STEP = 2

    def do(self):
        assert self.computer.outputs is not None
        addresses = param_addresses(
            self.computer.data, self.computer.i, self.read_modes, self.I_STEP - 1
        )
        self.computer.outputs.append(self.computer.data[addresses[0]])


class JumpTrueState(State):
    I_STEP = 3

    def do(self):
        addresses = param_addresses(
            self.computer.data, self.computer.i, self.read_modes, self.I_STEP - 1
        )
        if self.computer.data[addresses[0]] != 0:
            self.computer.i = (
                self.computer.data[addresses[1]] - self.I_STEP
            )  # subtract I_STEP because super class will add I_STEP


class JumpFalseState(State):
    I_STEP = 3

    def do(self):
        addresses = param_addresses(
            self.computer.data, self.computer.i, self.read_modes, self.I_STEP - 1
        )
        if self.computer.data[addresses[0]] == 0:
            self.computer.i = (
                self.computer.data[addresses[1]] - self.I_STEP
            )  # subtract I_STEP because super class will add I_STEP


class CmpLessState(State):
    I_STEP = 4

    def do(self):
        addresses = param_addresses(
            self.computer.data, self.computer.i, self.read_modes, self.I_STEP - 1
        )
        self.computer.data[addresses[2]] = (
            1 if self.computer.data[addresses[0]] < self.computer.data[addresses[1]] else 0
        )


class CmpEqualsState(State):
    I_STEP = 4

    def do(self):
        addresses = param_addresses(
            self.computer.data, self.computer.i, self.read_modes, self.I_STEP - 1
        )
        self.computer.data[addresses[2]] = (
            1 if self.computer.data[addresses[0]] == self.computer.data[addresses[1]] else 0
        )


class AdjustRelBaseState(State):
    I_STEP = 2

    def do(self):
        addresses = param_addresses(
            self.computer.data, self.computer.i, self.read_modes, self.I_STEP - 1
        )
        self.computer.rbase += self.computer.data[addresses[0]]


def parse_code(code):
    cstr = str(code)
    return int(cstr[-2:]), tuple(ParamMode(int(c)) for c in reversed(cstr[:-2]))


def test_parse_code():
    assert parse_code(2) == (2, ())
    assert parse_code(3) == (3, ())
    assert parse_code(1002) == (2, (ParamMode.POSITION, ParamMode.DIRECT))
    assert parse_code(11003) == (
        3,
        (ParamMode.POSITION, ParamMode.DIRECT, ParamMode.DIRECT),
    )


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
            9: AdjustRelBaseState,
            99: None,
        }
        cmd, modes = parse_code(self.computer.data[self.computer.i])
        state = COMMAND_MAP[cmd]
        return state(self.computer, read_modes=modes) if state else None


class Computer:
    def __init__(self, mem, inputs=None, run=True):
        self.data = mem.copy()
        self.i = 0
        self.rbase = 0
        self.inputs = inputs
        self.outputs = []
        self.current_state = ExecState(self)
        if run:
            self.run()

    def run(self, partial=False):
        # return value of False means that we have not reached the halt (99) state yet
        while self.current_state:
            try:
                self.current_state.do()
            except IntCodeNoInputError as e:
                if not partial:
                    raise e
                else:
                    return False
            self.current_state = self.current_state.next_state()
        return True


def compute(mem, inputs=None):
    c = Computer(mem, inputs)
    return c.data, c.outputs


def test_compute():
    assert compute([1001, 0, 0, 3, 99]) == ([1001, 0, 0, 1001, 99], [])
    assert compute([1002, 0, 3, 3, 99]) == ([1002, 0, 3, 3006, 99], [])
    assert compute([3, 1, 99], [-5]) == ([3, -5, 99], [])
    assert compute([3, 1, 3, 2, 99], [-5, -6]) == ([3, -5, -6, 2, 99], [])
    with pytest.raises(IntCodeNoInputError):
        compute([3, 1, 99], [])
    assert compute([4, 0, 99]) == ([4, 0, 99], [4])
    assert compute([104, 86, 99]) == ([104, 86, 99], [86])
    assert compute([1105, 0, 300, 99]) == ([1105, 0, 300, 99], [])
    assert compute([1105, 13, 6, -1, -1, -1, 99]) == ([1105, 13, 6, -1, -1, -1, 99], [])
    assert compute([1106, 13, 300, 99]) == ([1106, 13, 300, 99], [])
    assert compute([1108, 1, 1, 5, 99, -1]) == ([1108, 1, 1, 5, 99, 1], [])
    assert compute([108, -1, 5, 6, 99, -1, -1]) == ([108, -1, 5, 6, 99, -1, 1], [])
    assert compute([1107, 1, 2, 5, 99, -1]) == ([1107, 1, 2, 5, 99, 1], [])
    assert compute([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], [0]) == (
        [3, 3, 1105, 0, 9, 1101, 0, 0, 12, 4, 12, 99, 0],
        [0],
    )


def test_relative_base_adjustment():
    c = Computer([109, 19, 99])
    assert c.rbase == 19
    c = Computer([109, 1, 109, -5, 99])
    assert c.rbase == -4


if __name__ == "__main__":
    pass
