from dataclasses import dataclass
import typing


@dataclass
class Node:
    id: str
    orbiting: typing.Type["Node"]
    #satellites: typing.List[typing.Type["Node"]] = None


if __name__ == '__main__':
    pass