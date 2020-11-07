from helpers import get_input
from random import random

import logging
logging.basicConfig(level=logging.INFO)

class OffMap(Exception):
    pass


class Drop(object):

    def __init__(self, position, map):
        self.position = position
        self.map = map

    def down(self):
        return (self.position[0], self.position[1]+1)

    def left(self):
        return (self.position[0]-1, self.position[1])

    def right(self):
        return (self.position[0]+1, self.position[1])

    def visit(self):
        assert self.map.can_visit(self.position)
        self.map.set(self.position, Map.VISITED)

    def settled(self):
        return not (
            self.map.can_visit(self.left()) or
            self.map.can_visit(self.right()) or
            self.map.can_visit(self.down())
        )

    def flow(self):
        self.fall()
        self.settle()

    def fall(self):
        pos = self.down()
        while self.map.can_visit(pos):
            self.position = pos
            self.visit()
            pos = self.down()

    def _pick_direction(self):
        if not self.map.can_visit(self.left()):
            return self.right
        if not self.map.can_visit(self.right()):
            return self.left
        else:
            return self.right if random()<=0.5 else self.left

    def track(self, direction):
        pos = direction()
        while self.map.can_visit(pos):
            if self.map.off_map(self.down()):
                raise OffMap()
            self.position = pos
            self.visit()
            if self.map.can_visit(self.down()):
                return False
            pos = direction()
        return True

    def settle(self):
        entry = self.position
        direction = self._pick_direction()
        try:
            if not self.track(direction):
                return self.flow()
            left = self.position
            direction = self.left if direction == self.right else self.right
            if not self.track(direction):
                return self.flow()
        except OffMap:
            return
        right = self.position
        if right < left:
            right, left = left, right
        self.fill(left, right)
        self.position = entry[0], entry[1]-1

    def fill(self, left, right):
        x0, y = left
        x1, _ = right
        assert all(self.map.can_visit((x,y)) for x in xrange(x0, x1+1))
        [self.map.set((x, y), Map.SETTLED) for x in xrange(x0, x1+1)]




class Map(object):

    SPRING = '+'
    SAND = '.'
    VISITED = '|'
    CLAY = '#'
    SETTLED = '~'

    def __init__(self, offset, dims):
        self.offset = offset
        self.limits = (offset[0]+dims[0], offset[1]+dims[1])
        self.layout = [[Map.SAND for _ in xrange(dims[0])] for _ in xrange(dims[1])]
        self.spring = (500, 0)
        self.set(self.spring, Map.SPRING)

    def __str__(self):
        return "\n".join(''.join(row) for row in self.layout)

    def visited(self):
        return sum(sum(1 for i in row if i in (Map.VISITED, Map.SETTLED)) for row in self.layout)

    def populate(self, items):
        for item in items:
            if isinstance(item[0], int):
                x = item[0]
                for y in xrange(item[1][0], item[1][1]+1):
                    self.set((x,y), Map.CLAY)
            else:
                y = item[1]
                for x in xrange(item[0][0], item[0][1]+1):
                    self.set((x,y), Map.CLAY)

    def off_map(self, pos):
        return (
            pos[0] < self.offset[0] or
            pos[0] >= self.limits[0] or
            pos[1] < self.offset[1] or
            pos[1] >= self.limits[1]
        )

    def get(self, position):
        return self.layout[
            position[1]-self.offset[1]][
            position[0]-self.offset[0]]

    def set(self, position, type):
        self.layout[
            position[1]-self.offset[1]][
            position[0]-self.offset[0]] = type

    def can_visit(self, pos):
        return (
            not self.off_map(pos) and
            self.get(pos) in (Map.SAND, Map.VISITED)
        )

    def drip(self):
        return Drop(self.spring, self)


def parse_line(line):
    #print line
    a, b = (x.split('=')[1] for x in line.split(', '))
    a = int(a)
    b = map(int, b.split('..'))
    if line[0] == 'y':
        a, b = b, a
    #print a, b
    return (a, b)


def get_dimensions(lines):
    mins = [None, 0]
    maxs = [None, None]
    for x, y in lines:
        minx = x if isinstance(x, int) else x[0]
        if mins[0] is None or minx < mins[0]:
            mins[0] = minx
        maxx = x if isinstance(x, int) else x[1]
        if maxs[0] is None or maxx > maxs[0]:
            maxs[0] = maxx
        maxy = y if isinstance(y, int) else y[1]
        if maxs[1] is None or maxy > maxs[1]:
            maxs[1] = maxy
    #print mins, maxs
    dims = [maxs[0]-mins[0]+2, maxs[1]+1]
    return mins, dims

def demo(map):
    for _ in xrange(80):
        map.drip().flow()
        #print str(map)
    print str(map)
    return map.visited()


def run(map):
    same = 0
    while True:
        old = str(map)
        map.drip().flow()
        if str(map) == old:
            same += 1
            if same >= 100:
                break
        else:
            same = 0
        logging.info("%s, %s", map.visited(), same)
        #print str(map)
    print str(map)
    return map.visited()


def part1():
    inputs = get_input(17)#, 'test')
    items = [parse_line(l) for l in inputs]
    offset, dims = get_dimensions(items)
    #print offset, dims
    map = Map(offset, dims)
    map.populate(items)
    #print str(map)
    #return demo(map)
    return run(map)

def main():
    print part1()


if __name__ == '__main__':
    main()
