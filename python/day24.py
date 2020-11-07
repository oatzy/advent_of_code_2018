import re
from functools import partial
from itertools import takewhile

from helpers import get_input

pattern = re.compile(r"(\d+) units each with (\d+) hit points (\(.+\))? ?"
                     r"with an attack that does (\d+) (\w+) damage at initiative (\d+)")
weak_pttn = re.compile(r"(immune|weak) to ([\w ,]+)")


class Group(object):

    IMMUNE = 'immune'
    INFECTION = 'infection'

    def __init__(self, type, units, hp, weak, immune, attack_power, attack_type, initiative):
        self.type = type
        self.units = int(units)
        self.hp = int(hp)
        self.weak = weak
        self.immune = immune
        self.attack_power = int(attack_power)
        self.attack_type = attack_type
        self.initiative = int(initiative)
    
    def __str__(self):
        return str(self.__dict__)
    
    def __repr__(self):
        return repr(self.__dict__)
    
    @property
    def effective_power(self):
        return self.units * self.attack_power
    
    def calculate_damage(self, target):
        if target.type == self.type:
            return 0
        if self.attack_type in target.immune:
            return 0
        damage = self.effective_power
        if self.attack_type in target.weak:
            damage *= 2
        return damage
    
    def select_target(self, targets):
        possible = []
        for t in targets:
            damage = self.calculate_damage(t)
            if damage == 0:
                continue
            possible.append((t, damage))
        if not possible:
            return None
        possible.sort(key=lambda x: (x[1], x[0].effective_power, x[0].initiative), reverse=True)
        #print possible
        return possible[0][0]
    
    def attack(self, target):
        damage = self.calculate_damage(target)
        #print "doing damage", damage
        killed = damage // target.hp
        target.units = max(0, target.units - killed) 


def parse_line(type, line):
    groups = list(pattern.match(line).groups())
    weakgrp = groups[2] or ''
    weak, immune = [], []
    for g in weak_pttn.findall(weakgrp):
        if g[0] == 'weak':
            weak = g[1].split(', ')
        if g[0] == 'immune':
            immune = g[1].split(', ')
    groups[2:3] = [weak, immune]
    return Group(type, *groups)


def parse_input(lines, boost=0):
    lines = iter(lines)
    next(lines)
    immune = map(partial(parse_line, Group.IMMUNE), takewhile(lambda x: x, lines))
    for g in immune:
        g.attack_power += boost
    #next(lines)
    next(lines)
    infect = map(partial(parse_line, Group.INFECTION), lines)
    return immune + infect


def fight(groups):
    groups.sort(key=lambda x: (x.effective_power, x.initiative), reverse=True)
    targets = [g for g in groups]
    #print groups

    pairings = []

    for group in groups:
        target = group.select_target(targets)
        #print "matched", group, target
        pairings.append((group, target))
        targets = [t for t in targets if id(t) != id(target)]
    
    pairings.sort(key=lambda x: x[0].initiative, reverse=True)

    for attack, defend in pairings:
        #print "attacker:", attack.type, attack.attack_type
        if defend is None:
            #print "no target"
            continue
        if attack.units <= 0:
            #print "already dead"
            continue
        #print "target:", defend.type, defend.attack_type
        before = defend.units
        attack.attack(defend)
        #print "killed", before - defend.units
    
    return [g for g in groups if g.units > 0]


def game_over(groups):
    return len(set(g.type for g in groups)) == 1


def run_fights(groups):
    round = 1
    before = sum(g.units for g in groups)
    while not game_over(groups):
        #print "round", round
        groups = fight(groups)
        round += 1
        after = sum(g.units for g in groups)
        if before == after:
            # deadlock
            break
        before = after
    return groups


def part1():
    inputs = get_input(24,'test')
    groups = parse_input(inputs)
    winners = run_fights(groups)
    print winners[0].type
    print [g.units for g in winners]

    return sum(g.units for g in winners)


def part2():
    boost = 0
    while True:
        print "boosted", boost
        inputs = get_input(24)#,'test')
        groups = parse_input(inputs, boost=boost)
        winners = run_fights(groups)
        if all(g.type == Group.IMMUNE for g in winners):
            return sum(g.units for g in winners)
        boost += 1


def main():
    #print part1()
    print part2()

if __name__ == '__main__':
    main()
