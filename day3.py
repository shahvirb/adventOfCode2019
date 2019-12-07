import inputreader
import collections

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


def intersection(a, b):
    """
    http://www.cs.swan.ac.uk/~cssimon/line_intersection.html
    >>> intersection(Line(Point(-1,0), Point(1,0)), Line(Point(0,-1), Point(0,1)))
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
        return Point(int(x_cross), int(y_cross))


def process_input(input):
    return [l.split(",") for l in input.splitlines()]


def part1(input):
    wires = make_wires(input)
    distances = crossings(wires)
    return min(distances)[0]


def crossings(wires):
    """
    >>> crossings([[Line(Point(-1,0), Point(1,0))], [Line(Point(0,-1), Point(0,1))]])
    [(0, Point(x=0, y=0))]
    >>> crossings([[Line(Point(0,0), Point(100,100))], [Line(Point(0,100), Point(100,0))]])
    [(100, Point(x=50, y=50))]
    >>> crossings([[Line(Point(0,0), Point(10,10)), Line(Point(10,10), Point(10,0))], [Line(Point(0,0), Point(0,5)), Line(Point(0,5), Point(15,5))]])
    [(10, Point(x=5, y=5)), (15, Point(x=10, y=5))]
    """
    distances = []
    for seg1 in wires[0]:
        for seg2 in wires[1]:
            cross = intersection(seg1, seg2)
            if cross:
                distances.append((manhattan(cross), cross))
    return distances


def make_wires(input):
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


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    input = inputreader.read("day3.txt")
    print(part1(input))
