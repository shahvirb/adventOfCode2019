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


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    input = inputreader.readlines("day1.txt")

    # Part 1
    masses = [int(i) for i in input]
    print(calc_fuel_sum(masses))

    # Part 2
    fuels = [calc_fuel_with_child_fuel(m) for m in masses]
    print(sum(fuels))
