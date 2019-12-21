import inputreader
from imaging import Image, image_to_text


def make_image(input):
    return Image(input, 25, 6)


def part1(input):
    img = make_image(input)
    counts = [l.count("0") for l in img.layers]
    pos = counts.index(min(counts))
    layer = img.layers[pos]
    return layer.count("1") * layer.count("2")


def part2(input):
    img = make_image(input)
    return image_to_text(img)


if __name__ == "__main__":
    input = inputreader.read("day8.txt")
    print(part1(input))
    print(part2(input))
