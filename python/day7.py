from helpers import get_input
from copy import deepcopy

class Task(object):

    def __init__(self, task, queue):
        self.task = task
        self.work = ord(task[0]) - 64 + 60
        self.done = False
        self._queue = queue

    def do_work(self):
        if self.done:
            return
        self.work -= 1
        if self.work <= 0:
            self.done = True
            self._queue._task_done(self.task)


class Queue(object):

    def __init__(self, tasks):
        self._queue = sorted(tasks.iteritems(), cmp=compare)
        self.counter = len(tasks)

    def _task_done(self, task):
        self.counter -= 1
        self._queue = remove_node(self._queue, task[0])

    def get_task(self):
        if not self._queue or self._queue[0][1]:
            return None
        task = Task(self._queue[0], self)
        self._queue = self._queue[1:]
        return task

    def done(self):
        return self.counter == 0


def parse_line(line):
    s = line.split()
    return s[1], s[7]


def build_nodes(pairs):
    nodes = {}
    for x, y in pairs:
        nodes.setdefault(y, set()).add(x)
        nodes.setdefault(x, set())
    return nodes


def compare(x, y):
    if len(x[1]) == len(y[1]):
        return 1 if x[0] > y[0] else -1
    return 1 if len(x[1]) > len(y[1]) else -1


def insert_node(nodes, n):
    nodes.append(n)
    for i in xrange(len(nodes)-2, -1, -1):
        if compare(nodes[i], n) < 1:
            break
        nodes[i], nodes[i+1] = nodes[i+1], nodes[i]
    return nodes


def remove_node(nodes, id_):
    new = []
    for n in nodes:
        if n[0] == id_:
            continue
        n[1].discard(id_)
        insert_node(new, n)
    return new


def order(nodes):
    nodes = sorted(nodes.iteritems(), cmp=compare)
    while nodes:
        top = nodes[0][0]
        yield top
        nodes = remove_node(nodes, top)


def part1(nodes):
    return "".join(order(nodes))


def part2(nodes):
    queue = Queue(nodes)
    workers = [None] * 5
    t = -1
    while not queue.done():
        for task in workers:
            if task is not None:
                task.do_work()
        for inx, task in enumerate(workers):
            if task is None or task.done:
                workers[inx] = queue.get_task()
        print ['.' if task is None else task.task[0] for task in workers]
        t += 1
    return t


def main():
    inputs = get_input(7)#, 'test')
    nodes = build_nodes(parse_line(line) for line in inputs)
    #print nodes
    #print part1(nodes)
    print part2(nodes)

if __name__ == '__main__':
    main()
