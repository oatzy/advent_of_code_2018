from collections import namedtuple
from datetime import datetime, timedelta
from helpers import get_input


sleep = namedtuple('sleep', 'id start length')

SLEEP = object()
WAKE = object()

class Shift(object):
    def __init__(self, id):
        self.id = id


def parse_line(line):
    time, event = line.split('] ')
    time = datetime.strptime(time[1:], "%Y-%m-%d %H:%M")
    #if time.hour == 23:
    #    time = datetime(time.year, time.month, time.day) + timedelta(1)
    if event.startswith('falls'):
        event = SLEEP
    elif event.startswith('wakes'):
        event = WAKE
    else:
        event = Shift(int(event.split('#')[-1].split()[0]))
    return time, event


def get_sleeps(events):
    id = events[0][1].id
    inx = 1
    while inx < len(events):
        time, event = events[inx]
        if event is SLEEP:
            start = time.minute
            length = events[inx+1][0].minute - start
            yield sleep(id, start, length)
            inx += 1
        elif isinstance(event, Shift):
            id = event.id
        else:
            raise Exception("got unexpected event %r", event)
        inx += 1

def correlate(sleeps):
    elves = {}
    for s in sleeps:
        elves.setdefault(s.id, []).append(s)
    return elves

def longest_sleep(elves):
    return max(elves.items(), key=lambda x: sum(zip(*x[1])[2]))

def make_sleep_minutes(sleeps):
    hours = [0]*60
    for s in sleeps:
        for i in xrange(s[1], s[1]+s[2]):
            hours[i] += 1
    return hours


def get_max_hour(hours):
    max_hour = max(xrange(60), key=lambda x: hours[x])
    return max_hour, hours[max_hour]


def part1(elves):
    longest = longest_sleep(elves)
    hours = make_sleep_minutes(longest[1])
    max_hour, _ = get_max_hour(hours)
    return longest[0], max_hour

def part2(elves):
    max_count = -1
    max_elf = (None, None)
    for id, sleeps in elves.iteritems():
        hours = make_sleep_minutes(sleeps)
        max_hour, count = get_max_hour(hours)
        if count > max_count:
            max_count = count
            max_elf = (id, max_hour)
    return max_elf

def main():
    inputs = get_input(4)
    inputs.sort()
    events = [parse_line(l) for l in inputs]
    sleeps = list(get_sleeps(events))
    elves = correlate(sleeps)

    id, hour = part1(elves)
    print id, hour, id*hour

    id, hour = part2(elves)
    print id, hour, id*hour

if __name__ == '__main__':
    main()
