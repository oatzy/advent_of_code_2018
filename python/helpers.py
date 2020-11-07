import os

INPUTS_PATH = '/home/chris/advent_of_code/2018/inputs'


def get_input(day, kind='input'):
    path = os.path.join(INPUTS_PATH, "day%s-%s.txt" % (day, kind))

    #if not os.path.exists(path):
    #    fetch_input_file(day, kind)

    with open(path, 'r') as f:
        return f.read().splitlines()


def assertEqual(x, y):
    assert x == y, "%s != %s" % (x, y)
