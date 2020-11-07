from helpers import get_input
from day16 import Assembler


def run_program(assembler, ip, program):

    EOF = len(program)

    line = lambda: assembler.registers[ip]
    def incr(): assembler.registers[ip] += 1

    while True:
        print assembler.registers
        instruction = program[line()]
        fn = getattr(assembler, instruction[0])
        fn(*instruction[1:])
        if line()+1 >= EOF:
            break
        incr()
    print assembler.registers
    return assembler.registers[0]


def part1(ip, program):
    assembler = Assembler(6)
    return run_program(assembler, ip, program)

def part2(ip, program):
    assembler = Assembler(6)
    #assembler.registers[0] = 1
    x = 10551260  # register 1 settles on this value
    assembler.registers = [6, x, x, 3, 4, 3*x]
    #return run_program(assembler, ip, program)
    # if you manually work out the control flow
    # you find that it's calculating the sum of factors of x
    return sum(i for i in xrange(1, x) if not x%i)

def main():
    inputs = get_input(19)#, 'test')
    ip = int(inputs[0].split()[-1])
    program = [[line[0]] + map(int, line[1:]) for line in map(str.split, inputs[1:])]
    #print part1(ip, program)
    print part2(ip, program)

if __name__ == '__main__':
    main()
