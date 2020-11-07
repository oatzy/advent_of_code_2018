from helpers import get_input
from ast import literal_eval


class Assembler(object):

    _opmap = {}

    def __init__(self, registers=4):
        self.registers = [0] * registers

    # Addition
    def addr(self, ra, rb, rc):
        """addr (add register) stores into register C
        the result of adding register A and register B."""
        self.registers[rc] = self.registers[ra] + self.registers[rb]

    def addi(self, ra, b, rc):
        """addi (add immediate) stores into register C
        the result of adding register A and value B."""
        self.registers[rc] = self.registers[ra] + b

    # Multiplication
    def mulr(self, ra, rb, rc):
        """mulr (multiply register) stores into register C
        the result of multiplying register A and register B."""
        self.registers[rc] = self.registers[ra] * self.registers[rb]

    def muli(self, ra, b, rc):
        """muli (multiply immediate) stores into register C
        the result of multiplying register A and value B."""
        self.registers[rc] = self.registers[ra] * b

    # Bitwise AND
    def banr(self, ra, rb, rc):
        """banr (bitwise AND register) stores into register C
        the result of the bitwise AND of register A and register B."""
        self.registers[rc] = self.registers[ra] & self.registers[rb]

    def bani(self, ra, b, rc):
        """bani (bitwise AND immediate) stores into register C
        the result of the bitwise AND of register A and value B."""
        self.registers[rc] = self.registers[ra] & b

    # Bitwise OR
    def borr(self, ra, rb, rc):
        """borr (bitwise OR register) stores into register C
        the result of the bitwise OR of register A and register B."""
        self.registers[rc] = self.registers[ra] | self.registers[rb]

    def bori(self, ra, b, rc):
        """bori (bitwise OR immediate) stores into register C
        the result of the bitwise OR of register A and value B."""
        self.registers[rc] = self.registers[ra] | b

    # Assignment
    def setr(self, ra, _, rc):
        """setr (set register) copies the contents of register A into register C.
        (Input B is ignored.)"""
        self.registers[rc] = self.registers[ra]

    def seti(self, a, _, rc):
        """seti (set immediate) stores value A into register C.
        (Input B is ignored.)"""
        self.registers[rc] = a

    # Greater-than testing
    def gtir(self, a, rb, rc):
        """gtir (greater-than immediate/register) sets register C to 1
        if value A is greater than register B.
        Otherwise, register C is set to 0."""
        self.registers[rc] = int(a > self.registers[rb])

    def gtri(self, ra, b, rc):
        """gtri (greater-than register/immediate) sets register C to 1
        if register A is greater than value B.
        Otherwise, register C is set to 0."""
        self.registers[rc] = int(self.registers[ra] > b)

    def gtrr(self, ra, rb, rc):
        """gtrr (greater-than register/register) sets register C to 1
        if register A is greater than register B.
        Otherwise, register C is set to 0."""
        self.registers[rc] = int(self.registers[ra] > self.registers[rb])

    # Equality testing
    def eqir(self, a, rb, rc):
        """eqir (equal immediate/register) sets register C to 1
        if value A is equal to register B.
        Otherwise, register C is set to 0."""
        self.registers[rc] = int(a == self.registers[rb])

    def eqri(self, ra, b, rc):
        """eqri (equal register/immediate) sets register C to 1
        if register A is equal to value B.
        Otherwise, register C is set to 0."""
        self.registers[rc] = int(self.registers[ra] == b)

    def eqrr(self, ra, rb, rc):
        """eqrr (equal register/register) sets register C to 1
        if register A is equal to register B.
        Otherwise, register C is set to 0."""
        self.registers[rc] = int(self.registers[ra] == self.registers[rb])

    def execute(self, opcode, a, b, c):
        name = self._opmap[opcode]
        fn = getattr(self, name)
        fn(a, b, c)

def possible_ops(registers, op, expect):
    assembler = Assembler()
    poss = set()
    for name in dir(assembler):
        if name.startswith('_') or name == 'execute':
            continue
        fn = getattr(assembler, name)
        if not callable(fn):
            continue
        assembler.registers = registers[:]
        fn(*op[1:])
        if assembler.registers == expect:
            #print name
            poss.add(name)
    return poss


def deduce_codes(possibles):
    found = {}
    while possibles:
        #print possibles
        for code, ops in possibles.items():
            if len(ops) == 1:
                op = ops.pop()
                found[op] = code
                possibles.pop(code)
                #print op, code
                continue
            for op in list(ops):
                if op in found:
                    ops.remove(op)
    #print possibles
    return found


def test1():
    before = [3, 2, 1, 1]
    op = [9, 2, 1, 2]
    after = [3, 2, 2, 1]
    poss = possible_ops(before, op, after)
    assert len(poss) == 3, poss

def load_posibilities():
    inputs = get_input(16, 'part1')
    possibles = {}
    for i in xrange(0, len(inputs), 4):
        before = literal_eval(inputs[i].split(' ', 1)[-1])
        op = map(int, inputs[i+1].split())
        after = literal_eval(inputs[i+2].split(' ', 1)[-1][1:])
        possibles.setdefault(op[0], set()).update(possible_ops(before, op, after))
    return possibles

def part1():
    pos = load_posibilities()
    return sum(1 for ops in pos.values() if len(ops) >= 3)

def part2():
    possibles = load_posibilities()
    op_map = {v:k for k, v in deduce_codes(possibles).iteritems()}

    assembler = Assembler()
    assembler._opmap = op_map

    inputs = get_input(16, 'part2')
    for line in inputs:
        command = map(int, line.split())
        assembler.execute(*command)

    return assembler.registers[0]

def main():
    #test1()
    #print part1()
    print part2()

if __name__ == '__main__':
    main()
