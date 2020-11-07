from helpers import get_input


def get_metadata_inner(numbers):
    #print numbers
    child_count = numbers[0]
    meta_count = numbers[1]

    total = 0

    tail = numbers[2:]
    for _ in xrange(child_count):
        count, tail = get_metadata_inner(tail)
        total += count
    total += sum(tail[:meta_count])
    return total, tail[meta_count:]

def get_metadata_sum(numbers):
    total, _ = get_metadata_inner(numbers)
    return total


def get_child_inner(numbers):
    child_count = numbers[0]
    meta_count = numbers[1]

    children = {}

    tail = numbers[2:]

    for i in xrange(child_count):
        value, tail = get_child_inner(tail)
        children[i+1] = value
    if not children:
        total = sum(tail[:meta_count])
    else:
        total = sum(children.get(m, 0) for m in tail[:meta_count])

    return total, tail[meta_count:]

def get_root_value(numbers):
    value, _ = get_child_inner(numbers)
    return value

def part1(numbers):
    return get_metadata_sum(numbers)

def part2(numbers):
    return get_root_value(numbers)

def main():
    inputs = get_input(8)#, 'test')
    numbers = map(int, inputs[0].split())

    #print part1(numbers)
    print part2(numbers)

if __name__ == '__main__':
    main()
