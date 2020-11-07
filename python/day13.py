from helpers import get_input
from collections import deque
from itertools import cycle


class Collision(Exception):

    def __init__(self, first, second):
        self.first = first
        self.second = second


def bisect(s, x, low=0, high=None, key=lambda x: x):
    high = len(s) if high is None else high
    if low == high:
        return low
    pivot = low + (high - low) // 2
    value = key(s[pivot])
    if key(x) == value:
        raise Collision(s[pivot], x)
    if key(x) < value:
        return bisect(s, x, low, pivot, key)
    return bisect(s, x, pivot+1, high, key)


class PriorityQueue(object):

    def __init__(self, *args):
        self._queue = sorted(args, key=lambda x: x.position[::-1])

    def __iter__(self):
        return iter(self._queue)

    def __len__(self):
        return len(self._queue)

    def copy(self):
        return PriorityQueue(*self._queue)

    def insert(self, value):
        inx = bisect(self._queue, value, key=lambda x: x.position[::-1])
        self._queue.insert(inx, value)

    def remove(self, value):
        self._queue.remove(value)


class Cart(object):

    FORWARD = (0, 1)
    LEFT = (-1, 0)
    BACKWARD = (0, -1)
    RIGHT = (1, 0)

    directions = {
        '^': BACKWARD,
        '<': LEFT,
        'v': FORWARD,
        '>': RIGHT
    }

    def __init__(self, position, direction):
        self.position = position
        self.direction = Cart.directions.get(direction, direction)
        self._spinner = cycle([Cart.LEFT, Cart.FORWARD, Cart.RIGHT])

    def turn(self, direction):
        if direction == Cart.LEFT:
            self.direction = (self.direction[1], -self.direction[0])
        elif direction == Cart.RIGHT:
            self.direction = (-self.direction[1], self.direction[0])

    def advance(self, square):
        # turn and move
        if square == '/':
            if self.direction[0]:
                self.turn(Cart.LEFT)
            else:
                self.turn(Cart.RIGHT)
        elif square == '\\':
            if self.direction[0]:
                self.turn(Cart.RIGHT)
            else:
                self.turn(Cart.LEFT)
        elif square == '+':
            self.turn(self._spinner.next())
        # else - carry on
        self.position = (
            self.position[0]+self.direction[0],
            self.position[1]+self.direction[1]
        )


class Track(object):

    def __init__(self, layout, carts):
        self.layout = layout
        self.carts = carts

    def get(self, position):
        return self.layout[position[1]][position[0]]

    @classmethod
    def from_inital_map(cls, initial):
        carts = []
        layout = []
        for y, line in enumerate(initial):
            row = []
            for x, char in enumerate(line):
                if char in '^<v>':
                    carts.append(Cart((x, y), char))
                    char = '-' if char in '<>' else '|'
                row.append(char)
            layout.append(row)
        return cls(layout, PriorityQueue(*carts))

    def tick(self, remove_colliding=False):
        new_carts = self.carts.copy()
        for c in self.carts:
            if c not in new_carts:
                # already removed
                continue
            new_carts.remove(c)
            c.advance(self.get(c.position))
            try:
                new_carts.insert(c)
            except Collision as e:
                print e.first.position
                if not remove_colliding:
                    raise
                new_carts.remove(e.first)
        self.carts = new_carts

    def __str__(self):
        dirs = {
            Cart.LEFT: '<',
            Cart.RIGHT: '>',
            Cart.FORWARD: 'v',
            Cart.BACKWARD: '^'
        }
        copy = [row[:] for row in self.layout]
        for c in self.carts:
            copy[c.position[1]][c.position[0]] = dirs[c.direction]
        return "\n".join(''.join(row) for row in copy)


def part1(track):
    #print str(track)

    while True:
        #print [(c.position, c.direction) for c in track.carts]
        #print str(track)
        try:
            track.tick()
        except Collision as e:
            return e.first.position
            break


def part2(track):
    while len(track.carts) > 1:
        #print [c.position for c in track.carts]
        track.tick(remove_colliding=True)
        #print str(track)
    #track.tick()
    c = track.carts._queue[0]
    #print c.direction
    return c.position


def main():
    inputs = get_input(13)#, 'test2')
    track = Track.from_inital_map(inputs)
    #print part1(track)
    print part2(track)


if __name__ == '__main__':
    main()
