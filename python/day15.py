from collections import deque
from helpers import get_input

class Unit(object):

    ELF = 'E'
    GOBLIN = 'G'

    def __init__(self, type, position, hp=200, power=3):
        self.type = type
        self.position = position
        self.hp = hp
        self.power = power

    def attack(self, target):
        target.hp -= self.power

    @property
    def dead(self):
        return self.hp <= 0

    def inrange(self, other):
        return (abs(self.position.x - other.position.x) +
                abs(self.position.y - other.position.y)) == 1


class Cell(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "{0.__class__.__name__}({0.x}, {0.y})".format(self)

    def __eq__(self, other):
        return (self.x == other.x and self.y == other.y)

    def __add__(self, other):
        return Cell(self.x + other.x, self.y + other.y)

    def __gt__(self, other):
        return (self.y, self.x) > (other.y, other.x)


class Cave(object):

    FORWARD = Cell(0, 1)
    LEFT = Cell(1, 0)
    BACKWARD = Cell(0, -1)
    RIGHT = Cell(-1, 0)

    def __init__(self, layout, units):
        self.layout = layout
        self.units = units

    def __str__(self):
        units = {(u.position.x, u.position.y): u.type for u in self.units}
        lines = []
        for y, line in enumerate(self.layout):
            row = []
            for x, char in enumerate(line):
                row.append(units.get((x,y), char))
            lines.append("".join(row))
        return "\n".join(lines)

    @classmethod
    def from_strings(cls, lines, elf_power=3):
        units = []
        layout = []
        for y, line in enumerate(lines):
            row = []
            for x, char in enumerate(line):
                if char in 'EG':
                    power = elf_power if char == 'E' else 3
                    units.append(Unit(char, Cell(x, y), power=power))
                    char = '.'
                row.append(char)
            layout.append(row)
        return cls(layout, units)

    def get(self, position):
        return self.layout[position.y][position.x]

    def enemies_in_range(self, unit):
        enemies = []
        for u in self.units:
            if u.type == unit.type or u.dead:
                continue
            if unit.inrange(u):
                enemies.append(u)
        return enemies

    def empty(self, position):
        if self.get(position) == '#':
            return False
        for u in self.units:
            if not u.dead and u.position == position:
                return False
        return True

    def neighbours(self, position):
        return filter(self.empty, (position + d for d in
            [Cave.BACKWARD, Cave.LEFT, Cave.RIGHT, Cave.FORWARD]))

    def pick_target(self, enemies):
        return min(enemies, key=lambda e: (e.hp, e.position))

    def move(self, unit):
        p = PathFinder(self, unit)
        pos = p.find_next_move()
        #print unit.position, pos
        if pos is not None:
            unit.position = pos

    def iterate(self):
        self.units.sort(key=lambda x: x.position)
        for u in self.units:
            if u.dead:
                continue
            enemies = self.enemies_in_range(u)
            if not enemies:
                self.move(u)
                enemies = self.enemies_in_range(u)

            if not enemies:
                continue

            target = self.pick_target(enemies)

            u.attack(target)
        self.units = [u for u in self.units if not u.dead]

class PathFinder(object):

    def __init__(self, cave, unit):
        self.cave = cave
        self.unit = unit
        height = len(cave.layout)
        width = len(cave.layout[0])
        self.distances = [([None] * width) for _ in xrange(height)]

    def set(self, pos, distance):
        self.distances[pos.y][pos.x] = distance

    def get(self, pos):
        return self.distances[pos.y][pos.x]

    def find_next_move(self):
        min_distance = None
        targets = []
        q = deque()
        p0 = self.unit.position
        #print self.cave.neighbours(p0)
        q.extend(self.cave.neighbours(p0))
        while len(q):
            #print self.draw_distances()
            #print q
            p = q.popleft()
            neighbours = self.cave.neighbours(p)
            ndists = filter(None, (self.get(x) for x in neighbours))
            distance = min(ndists or [0]) + 1
            self.set(p, distance)
            if self.cave.enemies_in_range(Unit(self.unit.type, p)):
                if min_distance is None:
                    min_distance = distance
                if distance == min_distance:
                    targets.append(p)
            q.extend(n for n in neighbours if self.get(n) is None and n not in q)
        if targets:
            return self._backtrack(min(targets))
        return None

    def _backtrack(self, pos):
        #print self.draw_distances()
        while self.get(pos) != 1:
            pos = sorted((n for n in self.cave.neighbours(pos)
                          if self.get(n) == self.get(pos) - 1))[0]
        return pos

    def draw_distances(self):
        layout = [row[:] for row in self.cave.layout[:]]
        for y, row in enumerate(self.distances):
            for x, d in enumerate(row):
                if d is not None:
                    layout[y][x] = str(d)
        return "\n".join("".join(row) for row in layout)


def run(cave):
    t = 0
    while len(set(u.type for u in cave.units)) > 1:
        #print str(cave)
        cave.iterate()
        t += 1
    return t


class DeadElf(Exception):
    pass


def run_until_death(cave):
    elf_count = lambda: sum(1 for u in cave.units if u.type == Unit.ELF)
    total_elves = elf_count()
    t = 0
    while len(set(u.type for u in cave.units)) > 1:
        #print str(cave)
        cave.iterate()
        t += 1
        if elf_count() < total_elves:
            raise DeadElf()
    return t


def part1():
    inputs = get_input(15, 'test2')
    cave = Cave.from_strings(inputs)
    print str(cave)
    rounds = run(cave)
    print str(cave)
    hp = sum(u.hp for u in cave.units)
    print rounds, hp
    return rounds * hp

def part2():
    inputs = get_input(15)#, 'test2')
    power = 3
    while True:
        print power
        cave = Cave.from_strings(inputs, power)
        #print str(cave)
        try:
            rounds = run_until_death(cave)
        except DeadElf:
            power += 1
        else:
            break
        #print str(cave)
    print power
    hp = sum(u.hp for u in cave.units)
    print rounds, hp
    return rounds * hp

def main():
    #print part1()
    print part2()

if __name__ == '__main__':
    main()
