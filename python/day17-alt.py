from helpers import get_input
from random import random

CLAY = set()
SETTLED = set()
VISITED = set()

MAXY = 0
MINY = 0
SPRING = (500, 0)


class OffMap(Exception):
    pass


def down(pos):
    return (pos[0], pos[1]+1)

def left(pos):
    return (pos[0]+1, pos[1])

def right(pos):
    return (pos[0]-1, pos[1])

def can_visit(pos):
    return pos not in CLAY and pos not in SETTLED

def flow(pos):
    pos = fall(pos)
    settle(pos)

def fall(pos):
    while True:
        p = down(pos)
        if p[1] > MAXY:
            raise OffMap()
        if can_visit(p):
            VISITED.add(p)
        else:
            return pos
        pos = p

def pick_direction(pos):
    if not can_visit(left(pos)):
        return right
    if not can_visit(right(pos)):
        return left
    else:
        return right if random()<=0.5 else left

def track(pos, direction):
    nxt = direction(pos)
    while can_visit(nxt):
        pos = nxt
        VISITED.add(pos)
        if down(pos)[1] > MAXY:
            raise OffMap()
        if can_visit(down(pos)):
            return pos, True
        nxt = direction(pos)
    return pos, False

def settle(pos):
    entry = pos
    while True:
        direction = pick_direction(entry)
        try:
            pos_left, can_fall = track(entry, direction)
            if can_fall:
                return flow(pos_left)
            direction = left if direction == right else right
            pos_right, can_fall = track(pos_left, direction)
            if can_fall:
                return flow(pos_right)
        except OffMap:
            return

        if pos_right < pos_left:
            pos_right, pos_left = pos_left, pos_right
        fill(pos_left, pos_right)

        entry = (entry[0], entry[1]-1)

def fill(left, right):
    x0, y = left
    x1, _ = right
    #print x0, x1, y
    SETTLED.update((x, y) for x in xrange(x0, x1+1))


def stringify():
    points = SETTLED|VISITED|CLAY
    mins = map(min, zip(*points))
    maxs = map(max, zip(*points))
    mins[1] = 0

    layout = []
    for y in xrange(mins[1], maxs[1]+1):
        row = []
        for x in xrange(mins[0], maxs[0]+1):
            if (x,y) == SPRING:
                row.append('+')
            elif (x,y) in CLAY:
                row.append('#')
            elif (x,y) in SETTLED:
                row.append('~')
            elif (x,y) in VISITED:
                row.append('|')
            else:
                row.append('.')
        layout.append("".join(row))
    return '\n'.join(layout)


def state():
    return (len(CLAY), len(SETTLED), len(VISITED))


def run():
    same = 0
    while True:
        #print stringify()
        old = state()
        #print old
        flow(SPRING)
        if state() == old:
            same += 1
            if same >= 100:
                break
        else:
            same = 0
    return sum(1 for _,y in list(VISITED|SETTLED) if MINY <= y <= MAXY)

def set_maxy():
    global MAXY, MINY
    MAXY = max(y for _, y in CLAY)
    MINY = min(y for _, y in CLAY)


def parse_line(line):
    #print line
    a, b = (x.split('=')[1] for x in line.split(', '))
    a = int(a)
    b = map(int, b.split('..'))
    if line[0] == 'y':
        for x in xrange(b[0], b[1]+1):
            CLAY.add((x,a))
    else:
        for y in xrange(b[0], b[1]+1):
            CLAY.add((a,y))

def part1():
    inputs = get_input(17)#, 'test')
    for line in inputs:
        parse_line(line)
    set_maxy()

    res = run()
    #with open('day17.out', 'w') as f:
    #    f.write(stringify())
    return res
    
def part2():
    return sum(1 for _, y in list(SETTLED) if MINY <= y <= MAXY)


def main():
    print part1()
    print part2()


if __name__ == '__main__':
    main()
