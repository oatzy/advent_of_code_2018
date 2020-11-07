from collections import namedtuple, Counter
from string import letters
from helpers import get_input


Point = namedtuple("Point", "tag x y")


class Grid(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [None] * width * height

    @classmethod
    def from_points(cls, points):
        width = max(p.x for p in points) + 1
        height = max(p.y for p in points)+ 1

        grid = cls(width, height)
        return grid

    def populate(self, points):
        for x in xrange(self.width):
            for y in xrange(self.height):
                near = nearest(Point(None, x, y), points)
                if near is not None:
                    self.set_value(x, y, near.tag)

    def set_value(self, x, y, tag):
        self.grid[x + self.width*y] = tag

    def edges(self):
        s = set(self.grid[:self.width] + self.grid[-self.width:])
        for i in xrange(self.height):
            s.update([self.grid[self.width * i], self.grid[self.width * (i+1) - 1]])
        return s

    def print_grid(self):
        for i in xrange(self.height):
            print self.grid[i*self.width:(i+1)*self.width]


def distance(first, second):
    return abs(first.x - second.x) + abs(first.y - second.y)


def is_in_range(center, points, max_distance):
    dist = 0
    for p in points:
        dist += distance(center, p)
        if dist >= max_distance:
            return False
    return True


def nearest(center, points):
    distances = [(point, distance(center, point))
                 for point in points]
    distances.sort(key=lambda x: x[1])
    if distances[0][1] == distances[1][1]:
        return None
    return distances[0][0]


def load_points(inputs):
    for inx, line in enumerate(inputs):
        x,y = line.split(', ')
        yield Point(inx, int(x), int(y))


def part1(points):
    grid = Grid.from_points(points)
    grid.populate(points)

    exclude = grid.edges()
    counts = Counter(grid.grid)
    for e in exclude:
        counts.pop(e)
    return counts.most_common(1)


def part1_alt(points):
    c = Counter()
    exclude = set()

    width = max(p.x for p in points) + 1
    height = max(p.y for p in points) + 1

    def near(x, y, points):
        n = nearest(Point(None, x, y), points)
        return n and n.tag

    # edges
    for x in range(width):
        exclude.add(near(x, 0, points))
        exclude.add(near(x, height-1, points))
    for y in range(height):
        exclude.add(near(0, y, points))
        exclude.add(near(width-1, y, points))

    # body
    for x in range(1, width-1):
        for y in range(1, height-1):
            n = near(x, y, points)
            if n not in exclude:
                c.update([n])
    return c.most_common(1)


def part2(points):
    max_distance = 10000
    width = max(p.x for p in points) + 1
    height = max(p.y for p in points) + 1

    inrange = 0
    for x in xrange(width):
        for y in xrange(height):
            if is_in_range(Point(None, x, y), points, max_distance):
                inrange += 1
    return inrange


def main():
    inputs = get_input(6)
    points = list(load_points(inputs))

    #print part1(points)
    print part1_alt(points)
    #print part2(points)


if __name__ == '__main__':
    main()
