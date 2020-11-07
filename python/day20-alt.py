from collections import deque
from operator import itemgetter
from helpers import get_input, assertEqual


def move(pos, direction):
    if direction == 'N':
        return (pos[0], pos[1]-1)
    if direction == 'S':
        return (pos[0], pos[1]+1)
    if direction == 'E':
        return (pos[0]+1, pos[1])
    if direction == 'W':
        return (pos[0]-1, pos[1])


class Walker(object):

    def __init__(self, string):
        self.string = string
        self.distances = {(0,0): 0}

    def __str__(self):
        d = self.distances
        mins = map(min, zip(*d))
        maxs = map(max, zip(*d))

        return "\n".join(" ".join("% 2s" % (d.get((x,y), '.'))
            for x in xrange(mins[0], maxs[0]+1))
            for y in xrange(mins[1], maxs[1]+1))

    def _inner_walk(self, pos, offset):
        tasks = deque([(pos, offset)])
        while tasks:
            p, o = tasks.popleft()
            nodes, off = self._walk(p, o)
            tasks.extend((n, off) for n in nodes)
        return off

    def _walk(self, pos=(0,0), offset=0):
        i = offset
        nodes = set()

        cur = pos

        while i < len(self.string):
            c = self.string[i]
            print c, nodes

            if c == '(':
                i = self._inner_walk(cur, i+1)
                break
            elif c == ')':
                nodes.add(cur)
                i += 1
                break
            elif c == '|':
                nodes.add(cur)
                cur = pos
            else:
                nxt = move(cur, c)
                self.distances.setdefault(nxt, self.distances[cur]+1)
                cur = nxt
            i += 1
        return nodes, i


    def walk(self):
        self._walk()


def max_length(string):
    w = Walker(string[1:-1])
    w.walk()
    print str(w)
    return max(w.distances.values())


def test():
    assertEqual(max_length("^WNE$"), 3)
    assertEqual(max_length("^ENWWW(NEEE|SSE(EE|N))$"), 10)
    assertEqual(max_length("^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$"), 18)
    assertEqual(
        max_length("^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$"), 23)
    assertEqual(
        max_length("^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$"), 31
    )


def part1():
    max_length("^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$")
    return
    test()
    s = get_input(20)[0]
    return max_length(s)


def part2():
    pass

def main():
    print part1()
    #print part2()

if __name__ == '__main__':
    main()
