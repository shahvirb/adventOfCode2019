import inputreader
import collections
import dataclasses
import math

Point = collections.namedtuple("Point", "x y")
Line = collections.namedtuple("Line", "p1 p2")


def manhattan(p):
    """
    >>> manhattan(Point(1,-1))
    2
    """
    return abs(p.x) + abs(p.y)


def make_line(cmd, origin):
    DIRECTIONS = {
        "R": (1, 0),
        "U": (0, 1),
        "L": (-1, 0),
        "D": (0, -1),
    }
    cx, cy = DIRECTIONS[cmd[0]]
    magnitude = int(cmd[1:])
    p2 = Point(origin.x + magnitude * cx, origin.y + magnitude * cy)
    return Line(origin, p2)


def point_intersection(l, p):
    """
    >>> point_intersection(Line(Point(0,0), Point(0,1)), Point(1,0))
    False
    >>> point_intersection(Line(Point(0,0), Point(5,5)), Point(1,1))
    True
    >>> point_intersection(Line(Point(0,0), Point(5,5)), Point(-1,1))
    False
    >>> point_intersection(Line(Point(0,0), Point(5,5)), Point(-1,-1))
    False
    >>> point_intersection(Line(Point(10,-1), Point(0,-1)), Point(1,-1))
    True
    """
    denom = l.p2.x - l.p1.x
    if denom == 0:
        return p.x == l.p1.x and (l.p1.y <= p.y <= l.p2.y or l.p1.y >= p.y >= l.p2.y)
    lm = (l.p2.y - l.p1.y) / float(denom)
    lb = lm * (0 - l.p1.x) + l.p1.y
    y = lm * p.x + lb
    return (
        y == p.y
        and (l.p1.x <= p.x <= l.p2.x or l.p1.x >= p.x >= l.p2.x)
        and (l.p1.y <= p.y <= l.p2.y or l.p1.y >= p.y >= l.p2.y)
    )


def line_intersection(a, b):
    """
    http://www.cs.swan.ac.uk/~cssimon/line_intersection.html
    >>> line_intersection(Line(Point(-1,0), Point(1,0)), Line(Point(0,-1), Point(0,1)))
    Point(x=0, y=0)
    """
    x1 = a.p1.x
    y1 = a.p1.y
    x2 = a.p2.x
    y2 = a.p2.y

    x3 = b.p1.x
    y3 = b.p1.y
    x4 = b.p2.x
    y4 = b.p2.y

    denom = (x4 - x3) * (y1 - y2) - (x1 - x2) * (y4 - y3)
    if denom == 0:
        return None
    r = ((y3 - y4) * (x1 - x3) + (x4 - x3) * (y1 - y3)) / denom
    s = ((y1 - y2) * (x1 - x3) + (x2 - x1) * (y1 - y3)) / denom

    if 0 < r < 1 and 0 < s < 1:
        x_cross = x1 + (x2 - x1) * r
        y_cross = y1 + (y2 - y1) * r
        return Point(round(x_cross), round(y_cross))


def crossings(wires):
    distances = []
    for seg1 in wires[0]:
        for seg2 in wires[1]:
            cross = line_intersection(seg1, seg2)
            if cross:
                distances.append((manhattan(cross), cross))
    return distances


def make_wires(input):
    def process_input(input):
        return [l.split(",") for l in input.splitlines()]

    text_lines = process_input(input)
    wires = []
    for tl in text_lines:
        origin = Point(0, 0)
        segments = []
        for cmd in tl:
            new = make_line(cmd, origin)
            origin = new.p2
            segments.append(new)
        wires.append(segments)
    assert len(wires) == 2
    return wires


def part1(input):
    wires = make_wires(input)
    distances = crossings(wires)
    return min(distances)[0]


def length(p1, p2):
    """
    >>> length(Point(-1,-1), Point(-1,1))
    2
    """
    return int(math.sqrt((p2.x-p1.x)**2 + (p2.y - p1.y) ** 2))

def signal_delay(wire, crossing):
    """
    >>> signal_delay([Line(Point(0,0), Point(5,0))], Point(3,0))
    3
    >>> signal_delay([Line(Point(0,0), Point(5,0)), Line(Point(5,0), Point(5,5))], Point(5,1))
    6
    """

    if point_intersection(wire[0], crossing):
        return length(wire[0].p1, crossing)

    return signal_delay(wire[1:], crossing) + length(wire[0].p1, wire[0].p2)


def solve_p2(wires):
    """
    >>> solve_p2([[Line(Point(0,0), Point(5,0)), Line(Point(5,0), Point(5,5))], [Line(Point(0,0), Point(0,1)), Line(Point(0,1), Point(6,1))]])
    12
    >>> solve_p2([[Line(Point(0,0), Point(5,0)), Line(Point(5,0), Point(5,5))], [Line(Point(0,0), Point(0,1)), Line(Point(0,1), Point(6,1)), Line(Point(6,1), Point(6,2)), Line(Point(6,2), Point(0,2))]])
    12
    """
    distances = crossings(wires)
    steps = [sum([signal_delay(w, d[1]) for w in wires]) for d in distances]
    return min(steps)


def part2(input):
    wires = make_wires(input)
    return solve_p2(wires)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    input = inputreader.read("day3.txt")
    print(part1(input))
    print(part2(input))
