use std::char;
use std::collections::BTreeMap;
use std::collections::HashMap;
use std::format;
use std::fs;
use toml::Table;

/*
TODOs:

 * Parse inputs.toml into struct(s)
 * Run sample as test and compare to expected
 * Eliminate input parsing/day running boilerplate
 * Consider separate inputs for each day

Inputs is

- day:
  - input: <str>
  - part1:
    - sample: <str>
    - result: <u32>
  - part2:
    - sample: <str>
    - result: <u32>

Map over keys in Table, pull impl fn. from a Map, bob's you're uncle
*/

enum Part {
    One,
    Two,
}

type DayFn = fn(Part) -> fn(&str) -> u32;

const DAY1_P: DayFn = day1;
const DAY2_P: DayFn = day2;

fn main() {
    let days: BTreeMap<String, DayFn> =
        BTreeMap::from([("day1".to_string(), DAY1_P), ("day2".to_string(), DAY2_P)]);
    let inputs = fs::read_to_string("inputs.toml")
        .expect("Failed to read inputs.toml")
        .parse::<Table>()
        .expect("Failed to parse inputs.toml");

    days.iter().for_each(|(day, day_f)| {
        println!("Running {}", day);
        let day_inputs = inputs[day]
            .as_table()
            .expect(format!("{} is not a table", day).as_str());
        let input = day_inputs["input"].as_str().expect("missing input");
        let part1_sample = day_inputs["part1"].as_table().expect("missing part1")["sample"]
            .as_str()
            .expect("missing sample");
        let part2_sample = day_inputs["part2"].as_table().expect("missing part2")["sample"]
            .as_str()
            .expect("missing sample");

        println!("Part1 Sample {}", day_f(Part::One)(part1_sample));
        println!("Part1 {}", day_f(Part::One)(input));
        println!("Part2 Sample {}", day_f(Part::Two)(part2_sample));
        println!("Part1 {}", day_f(Part::Two)(input));
        println!();
    });
}

//////////////////////
// DAY 1
//////////////////////

fn day1(part: Part) -> fn(&str) -> u32 {
    match part {
        Part::One => |s| day1_impl(s, extract_numbers),
        Part::Two => |s| day1_impl(s, extract_numbers2),
    }
}

fn day1_impl(input: &str, extract_fn: fn(&str) -> Vec<u32>) -> u32 {
    input
        .lines()
        .map(extract_fn)
        .map(|v: Vec<u32>| match v.len() {
            0 => 0,
            _ => 10 * v[0] + v[v.len() - 1],
        })
        .sum()
}

fn extract_numbers(s: &str) -> Vec<u32> {
    s.matches(char::is_numeric)
        .map(|s| s.parse::<u32>().expect("Failed to parse char"))
        .collect()
}

fn extract_numbers2(s: &str) -> Vec<u32> {
    // Could do this by iterating on indices instead of mutating a slice
    let mut ssc = s.to_string();
    let mut sc = ssc.as_mut_str();
    let mut numbers = vec![];

    while sc.len() > 0 {
        let first = sc.chars().next().expect("Failed to get char");

        if char::is_numeric(first) {
            numbers.push(first.to_digit(10).expect("Failed to parse number"));
        } else {
            if sc.starts_with("one") {
                numbers.push(1);
            } else if sc.starts_with("two") {
                numbers.push(2);
            } else if sc.starts_with("three") {
                numbers.push(3);
            } else if sc.starts_with("four") {
                numbers.push(4);
            } else if sc.starts_with("five") {
                numbers.push(5);
            } else if sc.starts_with("six") {
                numbers.push(6);
            } else if sc.starts_with("seven") {
                numbers.push(7);
            } else if sc.starts_with("eight") {
                numbers.push(8);
            } else if sc.starts_with("nine") {
                numbers.push(9);
            }
        }

        sc = sc.get_mut(1..).expect("Failed to strip first char");
    }

    numbers
}

//////////////////////
// DAY 2
//////////////////////

#[derive(Clone, Copy, Debug)]
struct Cubes {
    blue_count: u32,
    green_count: u32,
    red_count: u32,
}

impl Cubes {
    fn fits_within(&self, other: &Self) -> bool {
        self.blue_count <= other.blue_count
            && self.green_count <= other.green_count
            && self.red_count <= other.red_count
    }
}

fn day2(part: Part) -> fn(&str) -> u32 {
    match part {
        Part::One => day2_impl,
        Part::Two => day2_impl,
    }
}

fn day2_impl(s: &str) -> u32 {
    let cubes = Cubes {
        blue_count: 14,
        green_count: 13,
        red_count: 12,
    };

    s.lines()
        .filter(|l| is_possible(*l, cubes))
        .map(|l| {
            l.get((l.find(" ").expect("Missing space") + 1)..l.find(":").expect("Missing colon"))
                .expect("No match?")
                .parse::<u32>()
                .expect("Not a number?")
        })
        .sum()
}

fn is_possible(game: &str, cubes: Cubes) -> bool {
    get_cubes(game).iter().all(|c| c.fits_within(&cubes))
}

fn get_cubes(game: &str) -> Vec<Cubes> {
    game.rsplit(":")
        .next()
        .expect("split on ':' failed")
        .split(";")
        .map(|s| {
            let cubes: HashMap<&str, u32> = s
                .split(",")
                .map(|s| {
                    let (count, color) = s
                        .trim()
                        .split_once(" ")
                        .expect("malformed count/color pair");
                    let cnt = count.trim().parse::<u32>().expect("malformed count");
                    (color.trim(), cnt)
                })
                .collect();

            Cubes {
                blue_count: *cubes.get("blue").unwrap_or(&0u32),
                green_count: *cubes.get("green").unwrap_or(&0u32),
                red_count: *cubes.get("red").unwrap_or(&0u32),
            }
        })
        .collect()
}
