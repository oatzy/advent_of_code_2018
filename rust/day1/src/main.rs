use std::fs::File;
use std::io::prelude::*;
use std::collections::HashSet;

struct Looper {
    items: Vec<isize>,
    len: usize,
    cur: usize
}

impl Looper {
    fn new(items: Vec<isize>) -> Looper {
        let len = items.len();
        Looper {
            items: items,
            len: len,
            cur: 0
        }
    }

    fn from_string(item_str: &str) -> Looper {
        let items = item_str.lines()
            .map(|f| f.parse::<isize>().unwrap())
            .collect();
        Looper::new(items)
    }
}

impl Iterator for Looper {
    type Item = isize;

    fn next(&mut self) -> Option<Self::Item> {
        let next = Some(self.items[self.cur]);
        self.cur += 1;
        if self.cur == self.len {
            self.cur = 0;
        }
        next
    }
}


fn part1(contents: &str) -> isize {
    contents.lines().map(|f| f.parse::<isize>().unwrap()).sum()
}

fn part2(contents: &str) -> isize {
    let mut seen = HashSet::new();
    let items = Looper::from_string(contents);
    let mut value = 0;
    seen.insert(0);
    for item in items {
        value += item;
        if seen.contains(&value) {
            return value;
        }
        seen.insert(value);
    }
    0
}


fn main() {
    let path = "/home/chris/advent_of_code2018/inputs/day1-input.txt";
    let mut f = File::open(path).expect("file not found");

    let mut contents = String::new();
    f.read_to_string(&mut contents)
        .expect("something went wrong reading the file");

    let freq1 = part1(&contents);
    let freq2 = part2(&contents);

    println!("part 1: {}\npart 2: {}", freq1, freq2);
}
