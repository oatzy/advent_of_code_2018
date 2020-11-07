from collections import Counter
from helpers import get_input


def counts(string):
    c = Counter(string)
    counts = c.values()
    return (2 in counts), (3 in counts)


def common_letters(first, seconds):
    return "".join(x for x, y in zip(first, seconds) if x == y)

def part1(input_):
    twos, threes = reduce(
        lambda x, y: (x[0]+y[0], x[1]+y[1]),
        map(counts, input_))
    return twos * threes


def part2(input_):
    for inx, first in enumerate(input_):
        for seconds in input_[inx+1:]:
            common = common_letters(first, seconds)
            if len(common) == len(first)-1:
                return common


def main():
    input_ = get_input(2)
    print part1(input_)
    print part2(input_)


def test():
    input_ = get_input(2, 'test')
    assert part1(input_) == 12


if __name__ == '__main__':
    main()
