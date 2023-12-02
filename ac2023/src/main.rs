use std::char;
use std::fs;
use toml::Table;

fn main() {
    let inputs = fs::read_to_string("inputs.toml")
        .expect("Failed to read day1.toml")
        .parse::<Table>()
        .expect("Failed to parse day1.toml");

    // TODO parse TOML into a struct
    let sample_out = part1(
        inputs["day1"].as_table().expect("day1 isn't a table")["part1"]
            .as_table()
            .expect("missing part1 for day1")["sample"]
            .as_str()
            .expect("missing day1.part1 sample")
            .to_string(),
    );
    let out = part1(
        inputs["day1"].as_table().expect("day1 isn't a table")["input"]
            .as_str()
            .expect("missing day1.input")
            .to_string(),
    );

    println!("Part1 sample: {}", sample_out);
    println!("Part1: {}", out);

    let sample_out = part2(
        inputs["day1"].as_table().expect("day1 isn't a table")["part2"]
            .as_table()
            .expect("missing part2 for day1")["sample"]
            .as_str()
            .expect("missing day1.part2 sample")
            .to_string(),
    );
    let out = part2(
        inputs["day1"].as_table().expect("day1 isn't a table")["input"]
            .as_str()
            .expect("missing day1.input")
            .to_string(),
    );

    println!("Part2 sample: {}", sample_out);
    println!("Part2: {}", out);
}

fn day1(input: String, extract_fn: fn(&str) -> Vec<u32>) -> u32 {
    input
        .as_str()
        .lines()
        .map(extract_fn)
        .map(|v: Vec<u32>| match v.len() {
            0 => 0,
            _ => 10 * v[0] + v[v.len() - 1],
        })
        .sum()
}

fn part1(input: String) -> u32 {
    day1(input, extract_numbers)
}

fn part2(input: String) -> u32 {
    day1(input, extract_numbers2)
}

fn extract_numbers(s: &str) -> Vec<u32> {
    s.matches(char::is_numeric)
        .map(|s| s.parse::<u32>().unwrap())
        .collect()
}

fn extract_numbers2(s: &str) -> Vec<u32> {
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
