from dataclasses import dataclass
import typing


@dataclass
class Node:
    id: str
    orbiting: typing.Type["Node"] = None
    # satellites: typing.List[typing.Type["Node"]] = None

    def __repr__(self):
        return self.id


def make_nodes(input):
    """
    >>> make_nodes("A)B")
    {'A': A, 'B': B}
    """

    def get_node(nodes, id):
        if id not in nodes:
            nodes[id] = Node(id)
        return nodes[id]

    all = {}
    for line in input.splitlines():
        ids = line.split(")")
        p = get_node(all, ids[0])
        s = get_node(all, ids[1])
        assert not s.orbiting
        s.orbiting = p
    return all


def distance(node, primary=None):
    if node.orbiting is None:
        return 0
    return 1 + distance(node.orbiting, primary)


def count_orbits(nodes, sun_id=None):
    d = 0
    i = 0
    sun = nodes.get(sun_id, None)
    for id in nodes:
        total = distance(nodes[id], sun)
        if total:
            d += 1
            i += total - 1
    return d, i


def part1(input):
    d, i = count_orbits(make_nodes(input), "COM")
    return d + i


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    import inputreader

    input = inputreader.read("day6.txt")
    # print(part1("COM)A\nA)B"))
    print(part1(input))
