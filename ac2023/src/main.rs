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
        inputs["day1"].as_table().expect("day1 isn't a table")["part1"]
            .as_table()
            .expect("missing part1 for day1")["input"]
            .as_str()
            .expect("missing day1.part1 sample")
            .to_string(),
    );

    println!("Part1 sample: {}", sample_out);
    println!("Part1: {}", out);
}

fn part1(input: String) -> u32 {
    input
        .as_str()
        .split("\n")
        .map(|s| {
            s.matches(char::is_numeric)
                .map(|s| s.parse::<u32>().unwrap())
                .collect()
        })
        .map(|v: Vec<u32>| match v.len() {
            0 => 0,
            _ => 10 * v[0] + v[v.len() - 1],
        })
        .sum()
}
