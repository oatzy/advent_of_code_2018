from helpers import get_input
from day16 import Assembler
from day19 import run_program

def max_run():
    # decompiled version of program
    possible = []
    x5 = 0
    while True:
        x4 = x5 | 65536
        x5 = 3935295
        while True:
            x2 = x4 & 255
            x5 += x2
            x5 = ((x5 & 16777215) * 65899) & 16777215
            if x4 < 256:
                break
            x4 /= 256
        print x5
        if x5 in possible:
            return possible[-1]
        possible.append(x5)

def part1():
    inputs = get_input(21)
    ip = int(inputs[0].split()[-1])
    program = [[line[0]] + map(int, line[1:]) for line in map(str.split, inputs[1:])]

    #assembler = Assembler(6)
    #x5 = run_once(assembler, ip, program)

    # sanity check
    assembler = Assembler(6)
    assembler.registers[0] = 16457176
    run_program(assembler, ip, program)


def part2():
    return max_run()

def main():
    #print part1()
    print part2()

if __name__ == '__main__':
    main()
