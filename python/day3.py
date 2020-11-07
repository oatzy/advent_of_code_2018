import re
from helpers import get_input
from collections import namedtuple

CLAIM_PTTN = re.compile("#(\d+) @ (\d+),(\d+): (\d+)x(\d+)")
claim = namedtuple("claim", "id x y w h")


class Board(object):

    def __init__(self, width, height):
        self.board = [0] * width * height
        self.width = width
        self.height = height

    def make_claim(self, claim):
        for x in xrange(claim.w):
            for y in xrange(claim.h):
                self.board[claim.x+x + self.width*(claim.y+y)] += 1

    def unique_claim(self, claim):
        for x in xrange(claim.w):
            for y in xrange(claim.h):
                if self.board[claim.x+x + self.width*(claim.y+y)] != 1:
                    return False
        return True

    def print_board(self):
        for y in xrange(self.height):
            print self.board[y*self.width:(y+1)*self.width]


def load_claims(inputs):
    return [claim(*map(int, CLAIM_PTTN.match(line).groups()))
            for line in inputs]


def get_dimensions(claims):
    width = max(c.x+c.w for c in claims)
    height = max(c.y+c.h for c in claims)
    return width, height


def make_claims(claims):
    width, height = get_dimensions(claims)
    board = Board(width, height)

    for c in claims:
        board.make_claim(c)

    return board


def part1(board):
    return sum(1 for count in board.board if count >= 2)


def part2(board, claims):
    for c in claims:
        if board.unique_claim(c):
            return c.id
    return None


def main():
    inputs = get_input(3)
    claims = load_claims(inputs)
    board = make_claims(claims)

    print part1(board)
    print part2(board, claims)


if __name__ == '__main__':
    main()
