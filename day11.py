import enum
import inputreader
import intcode
import collections
import operator
import imaging

Cartesian = collections.namedtuple("Cartesian", ["x", "y"])


class Direction(enum.Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


def change_direction_turn(i, dir):
    # if i == 1 then right turn elif i == 0 then left turn
    assert i == 0 or i == 1
    return Direction((dir.value + (1 if i == 1 else -1)) % 4)


def advance(pos, dir):
    MAP = {
        Direction.UP: (0, 1),
        Direction.RIGHT: (1, 0),
        Direction.DOWN: (0, -1),
        Direction.LEFT: (-1, 0),
    }
    dx, dy = MAP[dir]
    return Cartesian(pos.x + dx, pos.y + dy)


class PaintRobot:
    def __init__(self, code):
        self.position = Cartesian(0, 0)
        self.direction = Direction.UP
        self.computer = intcode.Computer(code, inputs=[], run=False)

    def go(self, camera_input):
        """
        :param camera_input: 0 if black, 1 if white
        :return: color to paint panel, turn direction, computer done running
        """
        assert not self.computer.inputs
        self.computer.inputs.append(camera_input)
        output_len_prev = len(self.computer.outputs)
        done = self.computer.run(partial=True)
        assert len(self.computer.outputs) - output_len_prev == 2
        return self.computer.outputs[-2], self.computer.outputs[-1], done


def paint_hull(code, initial_color):
    robot = PaintRobot(code)
    hull_paint = {robot.position: [initial_color]}
    # dict where key is Cartesian position and value is an array of paint colors
    done = False
    while not done:
        cam = 0 if robot.position not in hull_paint else hull_paint[robot.position][-1]
        paint, turn, done = robot.go(cam)
        # print(f"Painting pos={robot.position} color={paint} turn={turn}")
        hull_paint.setdefault(robot.position, []).append(paint)
        robot.direction = change_direction_turn(turn, robot.direction)
        robot.position = advance(robot.position, robot.direction)
    return hull_paint


def part1(input):
    code = inputreader.to_intcode(input)
    hull_paint = paint_hull(code, 0)
    return len(hull_paint)


def part2(input):
    code = inputreader.to_intcode(input)
    hull_paint = paint_hull(code, 1)
    # Calculate image size needed to represent hull
    min_x = min(hull_paint.keys(), key=operator.attrgetter("x")).x
    min_y = min(hull_paint.keys(), key=operator.attrgetter("y")).y
    max_x = max(hull_paint.keys(), key=operator.attrgetter("x")).x
    max_y = max(hull_paint.keys(), key=operator.attrgetter("y")).y
    # print((min_x, min_y), (max_x, max_y))
    width = max_x - min_x + 1
    height = max_y - min_y + 1
    # print(width, height)
    img = imaging.Image(["0"] * width * height, width, height)

    dx = 0 - min_x
    dy = 0 - min_y
    for pos, paints in hull_paint.items():
        img.layers[0].set(pos.x + dx, pos.y + dy, str(paints[-1]))

    # Flip the image about the y axis
    text = list(reversed(imaging.image_to_text(img).splitlines()))
    return f"\n".join(text)


if __name__ == "__main__":
    input = inputreader.read("day11.txt")
    print(part1(input))
    print(part2(input))
