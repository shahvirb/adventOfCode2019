import collections
import math

Cartesian = collections.namedtuple("Cartesian", ["x", "y"])
Polar = collections.namedtuple("Polar", ["r", "theta"])


def to_polar(cart, origin=None):
    x = origin.x if origin else 0
    y = origin.y if origin else 0
    dx = cart.x - x
    dy = cart.y - y
    r = math.sqrt(dx**2 + dy**2)

    try:
        t = math.degrees(math.atan(dy / float(dx)))
    except ZeroDivisionError as e:
        t = math.degrees(math.atan(dx / float(dy))) + 90 if dy > 0 else -90

    # adjust for quadrant
    if dx >= 0 and dy <= 0:
        t += 360
    elif dx >= 0 and dy >= 0:
        pass
    else:
        t += 180
    return Polar(r, t)


def test_to_polar():
    def verify(c, r, th):
        p = to_polar(c)
        assert p.r == r and p.theta == th

    verify(Cartesian(1, 1), math.sqrt(2), 45.0)
    verify(Cartesian(-1, 1), math.sqrt(2), 135.0)
    verify(Cartesian(-1, -1), math.sqrt(2), 225.0)
    verify(Cartesian(1, -1), math.sqrt(2), 315.0)
    verify(Cartesian(0, 1), 1, 90.0)
    verify(Cartesian(-1, 0), 1, 180.0)
    verify(Cartesian(0, -1), 1, 270.0)
    verify(Cartesian(1, 0), 1, 360.0)

    p = to_polar(Cartesian(5, 5), Cartesian(-5, 2))
    assert p.r == 10.44030650891055
    assert p.theta == 16.69924423399362


def make_objects(input):
    asteroids = []
    empty = [] #TODO why do the empties matter?
    containers = {"#": asteroids, ".": empty}
    for y, line in enumerate(input.splitlines()):
        for x, ch in enumerate(line):
            assert ch in containers
            containers[ch].append(Cartesian(x, y))
    assert (x + 1) * (y + 1) == len(asteroids) + len(empty)
    return asteroids, empty


def angles(origin, asteroids):
    angles = {}
    for ast in asteroids:
        if origin != ast:
            pc = to_polar(ast, origin)
            if pc.theta not in angles:
                angles[pc.theta] = []
            angles[pc.theta].append(pc)
    return angles


def part1(input):
    asteroids, empties = make_objects(input)
    counts = [(len(angles(a, asteroids).keys()), a) for a in asteroids]
    return max(counts)


if __name__ == "__main__":
    import inputreader

    input = inputreader.read("day10.txt")
    print(part1(input))
