extern crate priority_queue;
extern crate regex;
 
use priority_queue::PriorityQueue;
use regex::Regex;


fn main() {
    // an implementation of the 'wrong but correct' solution for part 2 (from reddit)
    let mut pq = PriorityQueue::new();
    
    let pttn = Regex::new(r"\d+").unwrap();
    
    let input = include_str!("/home/chris/advent_of_code2018/inputs/day23-input.txt");
    
    let bots = input.lines()
                .map(|line| {
                    let digits: Vec<isize> = pttn.find_iter(line).map(|x| x.as_str().parse().unwrap()).collect();
                    let bot: (isize, isize, isize, isize) = (digits[0], digits[1], digits[2], digits[3]);
                    bot
                });
    
    for bot in bots {
        let d = bot.0.abs() + bot.1.abs() + bot.2.abs();
        pq.push(((d-bot.3).max(0), 1), -(d-bot.3).max(0));
        pq.push((d+bot.3+1, -1), -(d+bot.3+1));
    }
    
    //println!("{}", pq.len());
    
    let mut count = 0;
    let mut max_count = 0;
    let mut result = 0;
    
    for ((dist, e), _) in pq.into_sorted_iter() {
        count += e;
        //println!("{}", count);
        if count > max_count {
            max_count = count;
            result = dist;
        }
    }
    
    println!("{}", result);
}
