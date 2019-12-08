import doctest


def has_same_adjacent(num):
    """
    >>> has_same_adjacent(1)
    False
    >>> has_same_adjacent(11)
    True
    >>> has_same_adjacent(1212)
    False
    >>> has_same_adjacent(123455678)
    True
    """

    def same_digits(digits):
        if len(digits) <= 1:
            return False
        if digits[0] == digits[1]:
            return True
        return same_digits(digits[1:])

    return same_digits(tuple(str(num)))


def has_double_digits(num):
    """
    >>> has_double_digits(111)
    False
    >>> has_double_digits(11122)
    True
    >>> has_double_digits(11222)
    True
    >>> has_double_digits(11123231)
    False
    >>> has_double_digits(181123231)
    True
    """
    digits = tuple("-" + str(num) + "-")
    for i in range(len(digits) - 3):
        if (
            digits[i + 1] == digits[i + 2]
            and digits[i] != digits[i + 1]
            and digits[i + 2] != digits[i + 3]
        ):
            return True
    return False


def has_increasing(num):
    """"
    >>> has_increasing(1)
    True
    >>> has_increasing(123)
    True
    >>> has_increasing(12123)
    False
    >>> has_increasing(122344)
    True
    """

    def increasing_digits(digits):
        if len(digits) <= 1:
            return True
        if digits[0] > digits[1]:
            return False
        return increasing_digits(digits[1:])

    return increasing_digits(tuple(str(num)))


"""
    Password Key Facts:
    KF1. It is a six-digit number.
    KF2. The value is within the range given in your puzzle input. (245318 - 765747)
    KF3. Two adjacent digits are the same (like 22 in 122345).
    KF4. Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).
"""
RANGE_LO = 245318
RANGE_HI = 765747


def count_solutions(constraint):
    count = 0
    for password in range(RANGE_LO, RANGE_HI + 1):
        if (
            len(str(password)) == 6
            and has_increasing(password)
            and constraint(password)
        ):
            count += 1
    return count


def part1_csp(unused):
    import constraint

    problem = constraint.Problem()
    problem.addVariable("password", range(RANGE_LO, RANGE_HI + 1))  # KF2
    problem.addConstraint(has_increasing, ("password",))  # KF4
    problem.addConstraint(has_same_adjacent, ("password",))  # KF3
    problem.addConstraint(lambda p: len(str(p)) == 6, ("password",))  # KF1
    sols = problem.getSolutions()
    return len(sols)


def part1_brute(unused):
    return count_solutions(has_same_adjacent)


def part2(unused):
    return count_solutions(has_double_digits)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(part1_brute(None))
    print(part2(None))
