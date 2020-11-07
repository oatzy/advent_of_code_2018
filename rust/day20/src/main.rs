use std::fs::File;
use std::io::prelude::*;
use std::ops::Add;
use std::collections::HashMap;


#[derive(Debug, Hash, Eq, PartialEq, Clone, Copy)]
struct Point {
    x: i32,
    y: i32,
}

impl Add for Point {
    type Output = Point;

    fn add(self, other: Point) -> Point {
        Point {
            x: self.x + other.x,
            y: self.y + other.y,
        }
    }
}

const N: Point = Point{x: 0, y: 1};
const S: Point = Point{x: 0, y: -1};
const E: Point = Point{x: 1, y: 0};
const W: Point = Point{x: -1, y: 0};


fn walk(pattern: String) -> HashMap<Point, usize> {
    let mut stack = Vec::new();
    let mut distances = HashMap::new();
    
    let pos = Point{x:0, y:0};
    let dist = 0;
    
    distances.insert(pos, 0);
    stack.push((pos, dist));
    
    for c in pattern.chars() {
        let (pos, dist) = stack.pop().expect("stack is unexpectedly empty");
        
        // println!("{:?} {}", pos, dist);
        
        let (pos, dist) = match c {
            'N' => (pos + N, dist+1),
            'S' => (pos + S, dist+1),
            'E' => (pos + E, dist+1),
            'W' => (pos + W, dist+1),
            '(' => {
                stack.push((pos, dist));
                (pos, dist)
            },
            ')' => stack.pop().expect("stack is unexpectedly empty").clone(),
            '|' => stack.last().expect("stack is unexpectedly empty").clone(),
            '^' | '$' => (pos, dist),
            _ => panic!("got unexpected character {}", c),
        };
        
        let dist = distances.entry(pos).or_insert(dist);
        
        stack.push((pos, *dist));
        
    }
    
    distances
    
}


fn main() {
    let path = "/home/chris/advent_of_code2018/inputs/day20-input.txt";
    let mut f = File::open(path).expect("file not found");

    let mut pattern = String::new();
    f.read_to_string(&mut pattern)
        .expect("something went wrong reading the file");
    pattern.pop();  // trailing newline
        
    //let pattern = String::from("^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$");
    
    let distances = walk(pattern);
    
    //println!("{:?}", distances);
    
    let (_, dist) = distances.iter().max_by_key(|x| x.1).unwrap();
    println!("{}", dist);
    
    let doors = distances.values().filter(|x| **x >= 1000).count();
    println!("{}", doors);
}
