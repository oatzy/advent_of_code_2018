from helpers import get_input

def part1():
    return sum(int(i) for i in get_input(1))


def input_looper():
    freqs = get_input(1)
    while True:
        for f in freqs:
            yield f


def part2():
    seen = set([0])
    value = 0
    for f in input_looper():
        value += int(f)
        if value in seen:
            return value
        seen.add(value)


if __name__ == '__main__':
    print part2()
