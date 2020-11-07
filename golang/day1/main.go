package main

import (
  "fmt"
  "io/ioutil"
  "strings"
  "strconv"
)

func part1(lines []string) int {
  total := 0;
  for _, line := range lines {
    value, err := strconv.Atoi(line)
    if err != nil {
      continue;
    }
    total += value;
  }
  return total;
}

func part2(lines []string) int {
  total := 0;
  seen := make(map[int]bool);
  seen[0] = true;
  for {
    for _, line := range lines {
      value, err := strconv.Atoi(line)
      if err != nil {
        continue;
      }
      total += value;
      if _, ok := seen[total]; ok {
        return total;
      }
      seen[total] = true;
    }
  }
  return total;
}

func main() {
  content, err := ioutil.ReadFile("/home/chris/advent_of_code2018/inputs/day1-input.txt");
  if err != nil {
    panic(err);
  }

  lines := strings.Split(string(content), "\n");

  fmt.Println(part1(lines));
  fmt.Println(part2(lines));

}
