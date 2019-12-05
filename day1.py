import inputreader
import doctest


def calc_fuel(m):
    """
    >>> calc_fuel(1969)
    654
    >>> calc_fuel(100756)
    33583
    """
    return int(m / 3) - 2


def calc_fuel_sum(inputs):
    return sum([calc_fuel(m) for m in inputs])


def calc_fuel_with_child_fuel(m):
    """
    >>> calc_fuel_with_child_fuel(14)
    2
    >>> calc_fuel_with_child_fuel(1969)
    966
    """
    fuel = calc_fuel(m)
    return 0 if fuel < 0 else fuel + calc_fuel_with_child_fuel(fuel)


def process_input(input):
    masses = [int(i) for i in [line.strip() for line in input.splitlines()]]
    return masses


def part1(input):
    return calc_fuel_sum(process_input(input))


def part2(input):
    fuels = [calc_fuel_with_child_fuel(m) for m in process_input(input)]
    return sum(fuels)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    input = inputreader.read("day1.txt")

    print(part1(input))
    print(part2(input))
