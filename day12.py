import inputreader
import numpy as np
import re
import itertools


class Moon:
    def __init__(self, x, y, z):
        self.pos = np.array([x, y, z])
        self.vel = np.zeros(3)

    def __repr__(self):
        return f"pos={self.pos}, vel={self.vel}"

    def apply_gravity(self, other):
        # Adjusts velocity according to gravity for self AND other
        def grav(a, b):
            delta = b - a
            return np.nan_to_num(delta / np.absolute(delta))

        g = grav(self.pos, other.pos)
        self.vel += g
        other.vel -= g

    def update_position(self):
        self.pos = self.pos + self.vel

    @property
    def potential_e(self):
        return np.sum(np.absolute(self.pos))

    @property
    def kinetic_e(self):
        return np.sum(np.absolute(self.vel))

    @property
    def total_e(self):
        return self.potential_e * self.kinetic_e


def make_moons(input):
    prog = re.compile(r"x=(-?[\d]*), y=(-?[\d]*), z=(-?[\d]*)")
    moons = []

    for line in input.splitlines():
        result = prog.search(line)
        moons.append(Moon(int(result[1]), int(result[2]), int(result[3])))
    return moons


def part1(input, stop=1000):
    moons = make_moons(input)
    combinations = [c for c in itertools.combinations(moons, 2)]

    for t in range(stop):
        for a, b in combinations:
            a.apply_gravity(b)

        print(t + 1)
        for m in moons:
            m.update_position()
            print(m)
    total = sum([m.total_e for m in moons])

    return total


if __name__ == "__main__":
    input = inputreader.read("day12.txt")
    print(part1(input, 1000))
