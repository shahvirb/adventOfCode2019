import inputreader


class Layer:
    def __init__(self, image, width, height, layer=0):
        self.image = image
        self.width = width
        self.height = height
        self.layer = layer

    @property
    def offset(self):
        return self.layer * self.width * self.height

    def at(self, x, y):
        i = self.offset + x + self.width * y
        return self.image[i]

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


class Image:
    def __init__(self, data, width, height):
        self.data = data
        num_layers = int(len(data) / (width * height))
        self.layers = [Layer(self.data, width, height, l) for l in range(num_layers)]


def part1(input):
    img = Image(input, 25, 6)
    counts = [l.count("0") for l in img.layers]
    pos = counts.index(min(counts))
    layer = img.layers[pos]
    return layer.count("1") * layer.count("2")


if __name__ == "__main__":
    input = inputreader.read("day8.txt")
    print(part1(input))
