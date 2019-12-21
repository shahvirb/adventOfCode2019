from enum import Enum


class Layer:
    def __init__(self, image, width, height, layer=0):
        self.image = image
        self.width = width
        self.height = height
        self.layer = layer

    @property
    def offset(self):
        return self.layer * self.width * self.height

    def index(self, x, y):
        return self.offset + x + self.width * y

    def at(self, x, y):
        return self.image[self.index(x, y)]

    def set(self, x, y, fill):
        self.image[self.index(x, y)] = fill

    def count(self, match):
        count = 0
        for p in self.image[self.offset : self.offset + self.width * self.height]:
            if p == match:
                count += 1
        return count


def test_layer():
    l1 = Layer("123456789012", 3, 2, 0)
    l2 = Layer("123456789012", 3, 2, 1)
    assert l1.at(0, 0) == "1"
    assert l1.at(1, 0) == "2"
    assert l1.at(0, 1) == "4"
    assert l2.at(2, 1) == "2"

    assert l1.count("1") == 1


class Color(Enum):
    BLACK = "0"
    WHITE = "1"
    TRANSPARENT = "2"


def visible(pixels):
    return visible(pixels[1:]) if Color(pixels[0]) == Color.TRANSPARENT else pixels[0]


def test_visible():
    assert visible(["0", "2", "1"]) == "0"
    assert visible(["2", "2", "1"]) == "1"


class Image:
    def __init__(self, data, width, height):
        self.data = data
        num_layers = int(len(data) / (width * height))
        self.layers = [Layer(self.data, width, height, l) for l in range(num_layers)]

    def at(self, x, y):
        pixels = [l.at(x, y) for l in self.layers]
        return visible(pixels)

    def rows(self):
        h = self.layers[0].height
        w = self.layers[0].width
        for y in range(h):
            row = ""
            for x in range(w):
                row += self.at(x, y)
            yield row


def image_to_text(img):
    dump = ""
    for row in img.rows():
        row = row.replace("0", " ")
        row = row.replace("1", "#")
        dump += f"{row}\n"
    return dump
