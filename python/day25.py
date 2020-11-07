from helpers import get_input
from collections import deque


def distance(first, second):
    return sum(abs(x-y) for x, y in zip(first, second))


def cluster_in_range(point, cluster):
    return any(distance(point, c) <= 3 for c in cluster)


def cluster(points):
    clusters = deque()

    for p in points:
        c = [p]
        length = len(clusters)
        for _ in xrange(length):
            if cluster_in_range(p, clusters[-1]):
                c.extend(clusters.pop())
            else:
                clusters.rotate()
        clusters.append(c)
    return clusters


def part1():
    inputs = get_input(25)#, 'test4')
    points = [map(int, line.split(',')) for line in inputs]
    constellations = cluster(points)
    #print constellations
    return len(constellations)


def main():
    print part1()


if __name__ == '__main__':
    main()
