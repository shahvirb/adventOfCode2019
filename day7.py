import inputreader
import intcode
import itertools


def calc_thruster_signal(software, phase_settings):
    last_output = 0
    for p in phase_settings:
        amp = intcode.Computer(software, inputs=[p, last_output])
        assert len(amp.outputs) == 1
        last_output = amp.outputs[0]
    return last_output


def test_calc_thruster_signal():
    assert (
        calc_thruster_signal(
            [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0],
            [4, 3, 2, 1, 0],
        )
        == 43210
    )
    assert (
        calc_thruster_signal(
            [
                3,
                23,
                3,
                24,
                1002,
                24,
                10,
                24,
                1002,
                23,
                -1,
                23,
                101,
                5,
                23,
                23,
                1,
                24,
                23,
                23,
                4,
                23,
                99,
                0,
                0,
            ],
            [0, 1, 2, 3, 4],
        )
        == 54321
    )
    assert (
        calc_thruster_signal(
            [
                3,
                31,
                3,
                32,
                1002,
                32,
                10,
                32,
                1001,
                31,
                -2,
                31,
                1007,
                31,
                0,
                33,
                1002,
                33,
                7,
                33,
                1,
                33,
                31,
                31,
                1,
                32,
                31,
                31,
                4,
                31,
                99,
                0,
                0,
                0,
            ],
            [1, 0, 4, 3, 2],
        )
        == 65210
    )


def solve(input, phase_lo, phase_hi, calc):
    software = inputreader.to_intcode(input)
    phases = itertools.permutations(list(range(phase_lo, phase_hi + 1)), 5)
    best = -1
    for phase in phases:
        best = max(calc(software, list(phase)), best)
    return best


def part1(input):
    return solve(input, 0, 4, calc_thruster_signal)


def calc_thruster_signal_feedback(software, phase_settings):
    inputs = [[p] for p in phase_settings]
    inputs[0].append(0)
    computers = [intcode.Computer(software, inputs=i, run=False) for i in inputs]
    last = computers[-1]
    while computers:
        c = computers.pop(0)
        done = c.run(partial=True)
        if len(computers) > 0:
            computers[0].inputs.append(c.outputs[-1])
        if not done:
            computers.append(c)
    return last.outputs[-1]


def test_calc_thruster_signal_feedback():
    assert (
        calc_thruster_signal_feedback(
            [
                3,
                26,
                1001,
                26,
                -4,
                26,
                3,
                27,
                1002,
                27,
                2,
                27,
                1,
                27,
                26,
                27,
                4,
                27,
                1001,
                28,
                -1,
                28,
                1005,
                28,
                6,
                99,
                0,
                0,
                5,
            ],
            [9, 8, 7, 6, 5],
        )
        == 139629729
    )
    assert (
        calc_thruster_signal_feedback(
            [
                3,
                52,
                1001,
                52,
                -5,
                52,
                3,
                53,
                1,
                52,
                56,
                54,
                1007,
                54,
                5,
                55,
                1005,
                55,
                26,
                1001,
                54,
                -5,
                54,
                1105,
                1,
                12,
                1,
                53,
                54,
                53,
                1008,
                54,
                0,
                55,
                1001,
                55,
                1,
                55,
                2,
                53,
                55,
                53,
                4,
                53,
                1001,
                56,
                -1,
                56,
                1005,
                56,
                6,
                99,
                0,
                0,
                0,
                0,
                10,
            ],
            [9, 7, 8, 5, 6],
        )
        == 18216
    )


def part2(input):
    return solve(input, 5, 9, calc_thruster_signal_feedback)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    input = inputreader.read("day7.txt")
    print(part1(input))
    print(part2(input))
