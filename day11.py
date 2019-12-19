import enum
import inputreader
import intcode
import collections

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


def part1(input):
    code = inputreader.to_intcode(input)
    robot = PaintRobot(code)
    hull_paint = {}
    # dict where key is Cartesian position and value is an array of paint colors

    done = False
    while not done:
        cam = 0 if robot.position not in hull_paint else hull_paint[robot.position][-1]
        paint, turn, done = robot.go(cam)
        print(f"Painting pos={robot.position} color={paint} turn={turn}")
        hull_paint.setdefault(robot.position, []).append(paint)
        robot.direction = change_direction_turn(turn, robot.direction)
        robot.position = advance(robot.position, robot.direction)

    return len(hull_paint)


if __name__ == "__main__":
    input = inputreader.read("day11.txt")
    print(part1(input))
