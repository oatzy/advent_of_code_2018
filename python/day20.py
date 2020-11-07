from helpers import get_input, assertEqual
from itertools import chain

_pairs = set([('N','S'), ('S', 'N'), ('E', 'W'), ('W', 'E')])

def cancel_append(s, x):
    if not s:
        s.append(x)
        return s
    if (x,s[-1]) in _pairs:
        s.pop()
    else:
        s.append(x)
    return s

def cancel_extend(s, t):
    for x in t:
        s = cancel_append(s, x)
    return s


def _max_length(string):
    longest = []
    current = []
    while True:

        c = next(string, None)
        #print c, current, longest
        if c is None:
            break

        if c == '(':
            l, string = _max_length(string)
            current = cancel_extend(current, l)
            #break
        elif c == ')':
            break
        elif c == '|':
            longest = max(current, longest, key=len)
            current = []
        else:
            current = cancel_append(current, c)
    l = max(current, longest, key=len)
    #print l
    return l, string


def max_length(string):
    longest, _ = _max_length(iter(string[1:-1]))
    return len(longest)


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
    #test()
    s = get_input(20)[0]
    return max_length(s)


def part2():
    pass

def main():
    #print part1()
    print part2()

if __name__ == '__main__':
    main()
