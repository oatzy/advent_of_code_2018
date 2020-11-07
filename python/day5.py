from helpers import get_input


class Node(object):

    def __init__(self, unit):
        self.kind = unit.lower()
        self.parity = unit.isupper()
        self.previous = None
        self.next = None

    def __str__(self):
        return self.kind.upper() if self.parity else self.kind


class LinkedList(object):

    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def add(self, unit):
        n = Node(unit)
        if self.head is None:
            self.head = self.tail = n
        else:
            self.tail.next = n
            n.previous = self.tail
            self.tail = n
        self.length += 1
        return n

    def remove(self, node):
        previous = node.previous
        next_ = node.next
        if previous is None:
            self.head = next_
            self.head.previous = None
            self.head.next.previous = self.head
        elif next_ is None:
            self.tail = previous
            self.tail.next = None
            self.tail.previous.next = self.tail
        else:
            previous.next = next_
            next_.previous = previous
        self.length -= 1
        return node

    @classmethod
    def from_string(cls, string):
        l = cls()
        for unit in string:
            l.add(unit)
        return l

    def __iter__(self):
        cur = self.head
        while cur is not None:
            yield str(cur)
            cur = cur.next

    def __str__(self):
        return "".join(self)


def react(polymer):
    previous = None
    current = polymer.head
    next_ = polymer.head.next

    while next_ is not None:
        #print str(polymer)
        #print str(previous), str(current), str(next_)
        if (current.kind == next_.kind and
                current.parity != next_.parity):

            polymer.remove(current)
            polymer.remove(next_)

            if previous is None:
                current = next_.next
                if current is None:
                    break
                next_ = current.next
                continue
            else:
                next_ = current.next.next
                current = previous
                previous = current.previous
        else:
            current = next_
            previous = current.previous
            next_ = current.next
    return polymer.length


def part1():
    input_ = get_input(5)[0]
    polymer = LinkedList.from_string(input_)
    #print str(polymer)
    length = react(polymer)
    #print str(polymer)
    return length


def part2():
    input_ = get_input(5)[0]
    units = sorted(set(input_.lower()))

    lengths = []

    for unit in units:
        inp = input_.replace(unit, '').replace(unit.upper(), '')
        lengths.append(react(LinkedList.from_string(inp)))

    return min(lengths)

def main():
    #print part1()
    print part2()

if __name__ == '__main__':
    main()
