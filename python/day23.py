import re
from collections import Counter
from operator import itemgetter
from helpers import get_input

pttn = re.compile("pos=<(\-?\d+),(\-?\d+),(\-?\d+)>, r=(\d+)")

def parse_line(line):
    return map(int, pttn.match(line).groups())

def max_range(bots):
    return max(bots, key=itemgetter(3))

def distance(first, second):
    return (
        abs(first[0]-second[0]) +
        abs(first[1]-second[1]) +
        abs(first[2]-second[2])
        )

def is_inrange(first, second):
    return distance(first, second) <= first[3]

def points_in_range(bot):
    x,y,z,r = bot
    return [(i,j,k)
        for i in xrange(x-r, x+r+1)
        for j in xrange(y-r, y+r+1)
        for k in xrange(z-r, z+r+1)
        if is_inrange(bot, (i,j,k))]

def shrink(bot, size):
    return [i//size for i in bot]

def grow(point, size):
    return [i*size for i in point]

def bots_in_range(point, bots):
    return sum(1 for b in bots if is_inrange(b, point))

def inrange_counter(point, bots):
    x,y,z = point
    return [((i,j,k), bots_in_range((i,j,k), bots))
            for i in xrange(x-10, x+11)
            for j in xrange(y-10, y+11)
            for k in xrange(z-10, z+11)]

def decluster(points):
    result = [points[0]]
    for p in points[1:]:
        if all(distance(x, p) >= 2 for x in result):
            result.append(p)
    return result

def part1(bots):
    maxbot = max_range(bots)
    return bots_in_range(maxbot, bots)

def part2(bots):
    # [103888940, 504903880, 464000100] <- current best
    top =  [(20,40,50)]
    for i in xrange(6,-1,-1):
        possible = set()
        scale = 10**i
        small_bots = [shrink(b, scale) for b in bots]
        for point in top:
            counts = inrange_counter(point, small_bots)
            counts.sort(key=itemgetter(1), reverse=True)
            possible.update(counts[:5])
        possible = sorted(possible, key=itemgetter(1), reverse=True)
        print possible
        top = ([x[0] for x in possible])[:5]
        print top
        top = [grow(t, 10) for t in top]
    top = [grow(x[0], 10) for x in possible if x[1] == possible[0][1]]
    print top
    return sum(sorted((x for x in top), key=lambda x: distance(x, (0,0,0)))[0])


def main():
    inputs = get_input(23)#, 'test')
    bots = [parse_line(l) for l in inputs]
    #print part1(bots)
    print part2(bots)

if __name__ == '__main__':
    main()
