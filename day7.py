import inputreader
import intcode
import itertools


def calc_thruster_signal(software, phase_settings):
    """
    >>> calc_thruster_signal([3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0], [4,3,2,1,0])
    43210
    >>> calc_thruster_signal([3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0], [0,1,2,3,4])
    54321
    >>> calc_thruster_signal([3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0], [1,0,4,3,2])
    65210
    """
    last_output = 0
    for p in phase_settings:
        amp = intcode.Computer(software, inputs=[p, last_output])
        assert len(amp.outputs) == 1
        last_output = amp.outputs[0]
    return last_output


def part1(input):
    software = inputreader.to_intcode(input)
    phases = itertools.permutations([0, 1, 2, 3, 4], 5)
    best = -1
    for phase in phases:
        best = max(calc_thruster_signal(software, list(phase)), best)
    return best


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    input = inputreader.read("day7.txt")
    print(part1(input))
