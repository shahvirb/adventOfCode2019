import collections
import math
import itertools
import operator

Cartesian = collections.namedtuple("Cartesian", ["x", "y"])
Polar = collections.namedtuple("Polar", ["r", "theta"])


def to_polar(cart, origin=None):
    x = origin.x if origin else 0
    y = origin.y if origin else 0
    dx = cart.x - x
    dy = cart.y - y
    r = math.sqrt(dx ** 2 + dy ** 2)

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


def to_cartesian(p, origin=None):
    def to_int(f):
        return int(
            round(f, 10)
        )  # 10 is arbitrary. Test empirically to see if it works.

    x = p.r * math.cos(math.radians(p.theta)) + origin.x if origin else 0
    y = p.r * math.sin(math.radians(p.theta)) + origin.y if origin else 0
    # print(x,y)
    return Cartesian(to_int(x), to_int(y))


def make_objects(input):
    asteroids = []
    for y, line in enumerate(input.splitlines()):
        for x, ch in enumerate(line):
            assert ch == "#" or ch == "."
            if ch == "#":
                asteroids.append(Cartesian(x, y))
    return asteroids


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
    asteroids = make_objects(input)
    counts = [(len(angles(a, asteroids).keys()), a) for a in asteroids]
    return max(counts)


def part2(input, stop=200):
    asteroids = make_objects(input)
    counts = [(len(angles(a, asteroids).keys()), a) for a in asteroids]
    count, best = max(counts)

    asteroid_angles = angles(best, asteroids)
    # Sort the asteroids by r so that they're vaporized from closest outwards
    for a in asteroid_angles:
        asteroid_angles[a] = sorted(asteroid_angles[a], key=operator.attrgetter("r"))

    all_angles = sorted(asteroid_angles.keys(), reverse=False)
    start_i = all_angles.index(270.0)
    angle_it = itertools.islice(itertools.cycle(all_angles), start_i, None)

    hits = 0

    while hits < stop:
        angle = next(angle_it)
        if len(asteroid_angles[angle]) > 0:
            hit_asteroid = asteroid_angles[angle].pop(0)
            hits += 1
            # print(f"{hits} best={best} hit_asteroid={hit_asteroid} {to_cartesian(hit_asteroid, best)}")

    hit_cart = to_cartesian(hit_asteroid, best)
    return hit_cart.x * 100 + hit_cart.y


if __name__ == "__main__":
    import inputreader

    input = inputreader.read("day10.txt")
    print(part1(input))
    print(part2(input, 200))
