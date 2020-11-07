from collections import deque


def play(players, rounds):
    board = deque([0])
    player = 0
    scores = {}

    for marble in xrange(1, rounds+1):

        player += 1
        if player == players+1:
            player = 1

        if not marble % 23:
            board.rotate(7)
            score = marble + board.pop()
            scores.setdefault(player, 0)
            scores[player] += score
            board.rotate(-1)
        else:
            board.rotate(-1)
            board.append(marble)
        #print player, board

    return max(scores.values())


def assertEqual(x, y):
    assert x == y, "%s != %s" % (x, y)


def test_part1():
    assertEqual(play(9, 32), 32)
    assertEqual(play(10, 1618), 8317)
    assertEqual(play(13, 7999), 146373)
    assertEqual(play(17, 1104), 2764)
    assertEqual(play(21, 6111), 54718)
    assertEqual(play(30, 5807), 37305)

def part1():
    #test_part1()
    #410 players; last marble is worth 72059 points
    high = play(410, 72059)
    return high

def part2():
    #410 players; last marble is worth 7205900 points
    high = play(410, 7205900)
    return high

def main():
    #print part1()
    print part2()

if __name__ == '__main__':
    main()
