from helpers import get_input


class Automata(object):

    def __init__(self, initial, transitions):
        self.state = initial
        self.transitions = transitions
        self.index = 0

    def _pad(self):
        linx = self.state.index('#')
        rinx = self.state[::-1].index('#')

        if linx < 4:
            self.state = (4-linx)*'.' + self.state
            self.index -= (4-linx)
        elif linx > 4:
            self.state = self.state[linx-4:]
            self.index += (linx-4)

        if rinx < 4:
            self.state = self.state + (4-rinx)*'.'
        elif rinx > 4:
            self.state = self.state[:4-rinx]

    def iterate(self):
        self._pad()
        new_state = ['.' '.']
        for i in xrange(2, len(self.state)-2):
            new_state.append(
                self.transitions.get(''.join(self.state[i-2:i+3]), '.')
            )
        self.state = "".join(new_state + ['.', '.'])

    def evolve(self, steps):
        last = self.state
        for i in xrange(steps):
            self.iterate()
            print self.index, self.state
            if last == self.state:
                self.index += (steps - i -1)
                break
            last = self.state

    def hashes(self):
        return [inx + self.index
                for inx, c in enumerate(self.state)
                if c == '#']


def part1(automata):
    #automata.iterate()
    automata.evolve(100)
    #print automata.index
    print automata.state
    h = automata.hashes()
    #print h
    return sum(h)


def part2(automata):
    #automata.iterate()
    automata.evolve(50000000000)
    #print automata.index
    print automata.state
    h = automata.hashes()
    #print h
    return sum(h)


def main():
    inputs = get_input(12)#, 'test')
    initial = inputs[0].split()[-1]
    #print initial
    transitions = dict(line.split(' => ') for line in inputs[2:])
    #print transitions
    automata = Automata(initial, transitions)
    #print part1(automata)
    print part2(automata)

if __name__ == '__main__':
    main()
