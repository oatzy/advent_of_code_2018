
class Elf(object):

    def __init__(self, index, board=None):
        self.index = index
        self._board = board

    @property
    def score(self):
        return self._board.scores[self.index]

    def advance(self):
        shift = self.score+1
        self.index = (self.index+shift) % len(self._board.scores)


class Board(object):

    def __init__(self, initial, elves=2):
        self.scores = initial
        self.elves = [Elf(i, self) for i in xrange(elves)]

    def __str__(self):
        out = []
        elves = [e.index for e in self.elves]
        for inx, s in enumerate(self.scores):
            if inx in elves:
                out.append('(%d)' % s)
            else:
                out.append(' %d ' % s)
        return "".join(out)

    def combine(self):
        score = sum(e.score for e in self.elves)
        self.scores += map(int, str(score))

    def iterate(self):
        self.combine()
        for e in self.elves:
            e.advance()

def demo(iterations):
    board = Board([3,7])
    print str(board)
    for _ in xrange(iterations):
        board.iterate()
        #print str(board)
    print str(board)


def next_ten(tries):
    board = Board([3, 7])
    target = tries + 10
    while len(board.scores) < target:
        board.iterate()
    return "".join(map(str, board.scores[tries:target]))


def count_before_score(target):
    board = Board([3, 7])
    target = str(target)
    tail = len(target) + 1
    while True:
        inx = ''.join(map(str, board.scores[-tail:])).find(target)
        if inx != -1:
            return len(board.scores) + inx - tail
        board.iterate()


def assertEqual(x, y):
    assert x == y, "%s != %s" % (x, y)

def test1():
    assertEqual(next_ten(5), "0124515891")
    assertEqual(next_ten(9), "5158916779")
    assertEqual(next_ten(18), "9251071085")
    assertEqual(next_ten(2018), "5941429882")

def test2():
    assertEqual(count_before_score("01245"), 5)
    assertEqual(count_before_score("51589"), 9)
    assertEqual(count_before_score("92510"), 18)
    assertEqual(count_before_score("59414"), 2018)


def part1():
    #demo()
    #test1()
    input_ = 380621
    return next_ten(input_)

def part2():
    #demo(10)
    #test2()
    input_ = "380621"
    return count_before_score(input_)

def main():
    #print part1()
    print part2()

if __name__ == '__main__':
    main()
