import numpy as np
from helpers import get_input


class Area(object):

    OPEN = '.'
    TREE = '|'
    LUMBER = '#'

    def __init__(self, layout):
        self.layout = layout

    def __str__(self):
        return "\n".join("".join(row) for row in self.layout)

    def neighbours(self, pos):
        square = self.layout[max(0, pos[0]-1):pos[0]+2, max(0, pos[1]-1):pos[1]+2]
        n = list(square.flatten())
        n.remove(self.layout[pos])
        return n

    def get_next_state(self, pos):
        s = self.layout[pos]
        n = self.neighbours(pos)
        if s == Area.OPEN and n.count(Area.TREE) >= 3:
            return Area.TREE
        if s == Area.TREE and n.count(Area.LUMBER) >= 3:
            return Area.LUMBER
        if s == Area.LUMBER and not (
                n.count(Area.LUMBER) and n.count(Area.TREE)
                ):
            return Area.OPEN
        return s

    def step(self):
        new = self.layout.copy()
        for y in xrange(new.shape[1]):
            for x in xrange(new.shape[0]):
                new[(x,y)] = self.get_next_state((x,y))
        self.layout = new

    def count(self, type):
        return sum(sum(1 for x in row if x == type) for row in self.layout)

def part1(area):
    #print str(area)
    for _ in xrange(10):
        area.step()
    #print str(area)
    wood = area.count(Area.LUMBER)
    trees = area.count(Area.TREE)
    print wood, trees
    return wood * trees

def part2(area):
    for t in xrange(100):
        area.step()
    while True:
        t += 1
        area.step()

        wood = area.count(Area.LUMBER)
        trees = area.count(Area.TREE)
        print t, wood, trees, wood*trees
    return wood * trees

def main():
    inputs = get_input(18)#, 'test')
    layout = np.array([list(i) for i in inputs])
    area = Area(layout)
    #print part1(area)
    print part2(area)

if __name__ == '__main__':
    main()
