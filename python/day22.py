from networkx import Graph
import networkx as nx

DEPTH = 4848 #510 #
TARGET = (15, 700) #(10, 10)#


def memoise(fn):
    store = {}
    def inner(x, y):
        if (x,y) in store:
            return store[(x,y)]
        return store.setdefault((x,y), fn(x, y))
    return inner


@memoise
def get_gi(x, y):
    #print x,y
    if (x,y) in ((0,0), TARGET):
        return 0
    if y == 0:
        return 16807*x
    if x == 0:
        return 48271*y
    a = get_erosion(x-1, y)
    b = get_erosion(x,y-1)
    return (a*b)


def get_erosion(x, y):
    return (get_gi(x,y) + DEPTH) % 20183


def get_type(x, y):
    t = get_erosion(x,y) % 3
    #print x, y, t
    return t


class Cost(object):
    NEITHER = 0
    TORCH = 1
    GEAR = 2


items = {
    Cost.TORCH: (0, 2),
    Cost.GEAR: (0, 1),
    Cost.NEITHER: (1, 2)
}

types = {
    0: (Cost.TORCH, Cost.GEAR),
    1: (Cost.GEAR, Cost.NEITHER),
    2: (Cost.NEITHER, Cost.TORCH)
}


def neighbours(x, y):
    for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:
        if (0<=x+dx<=TARGET[0]+100 and 0<=y+dy<=TARGET[1]+100):
            yield (x+dx, y+dy)


def build_graph():
    graph = Graph()
    for x in xrange(0, TARGET[0] + 101):
        for y in xrange(0, TARGET[1] + 101):
            typ = get_type(x, y)
            t1, t2 = types[typ]
            graph.add_edge((x,y,t1), (x,y,t2), weight=7)
            
            for x1, y1 in neighbours(x,y):
                typ1 = get_type(x1, y1)
                for item in (i for i in types[typ] if i in types[typ1]):
                    graph.add_edge((x,y,item), (x1,y1,item), weight=1)
    return graph


def part1():
    return sum(
        get_type(x,y)
        for y in xrange(TARGET[1]+1)
        for x in xrange(TARGET[0]+1)
    )


def part2():
    graph = build_graph()
    return nx.dijkstra_path_length(graph, (0,0,Cost.TORCH), (TARGET[0], TARGET[1], Cost.TORCH))


def main():
    #print part1()
    print part2()


if __name__ == '__main__':
    main()
