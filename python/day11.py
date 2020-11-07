
class Board(object):

    def __init__(self, size, serial):
        self.width = self.height = size
        self.serial = serial
        self.board = [self.get_level(i % size + 1, i // size + 1)
                      for i in xrange(size*size)]

    def get_level(self, x, y):
        r = x + 10
        p = (r * y) + self.serial
        p = (r * p)//100
        return (p % 10) - 5

    def square_sum(self, x, y, size):
        x, y = x - 1, y - 1
        return sum(sum(self.board[i*self.width + x: i*self.width + x + size])
                   for i in xrange(y, y+size))

    def boardify(self):
        return [self.board[i*self.width:(i+1)*self.width] for i in xrange(self.height)]

def max_sum(board, size):
    return max(((x, y) for x in xrange(1, board.width - size + 1)
               for y in xrange(1, board.height - size + 1)),
               key = lambda item: board.square_sum(item[0], item[1], size))

def max_sum_size(board):
    max_sum = 0
    max_coord = (0,0,0)

    x = 1
    y = 1

    while x <= board.width and y <= board.height:
        max_size = min(board.width - x, board.height - y)

        for size in xrange(1, max_size):
            value = board.square_sum(x, y, size)
            #print x, y, size, value
            if value < 0:
                x += size - 1
                break
            elif value > max_sum:
                max_sum = value
                max_coord = (x, y, size)
        x += 1
        if x > board.width:
            x = 1
            y += 1
    return max_coord

def brute_force(board):
    max_value = 0
    max_coord = (0,0,0)
    for x in xrange(225, 250):
        for y in xrange(125, 150):
            for size in xrange(10, 20):
                value = board.square_sum(x, y, size)
                if value > max_value:
                    max_value = value
                    max_coord = (x, y, size)
    return max_coord

def part1(board):
    return max_sum(board, 3)

def part2(board):
    #return max_sum_size(board)
    return brute_force(board)

def main():
    serial = 9306
    board = Board(300, serial)
    #print part1(board)
    print part2(board)


if __name__ == '__main__':
    main()
