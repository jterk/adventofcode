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

    println!("{}", sample_out)
}

fn part1(input: String) -> i64 {
    let stuff: Vec<String> = input
        .as_str()
        .split("\n")
        .map(|s| s.matches(char::is_numeric).collect::<Vec<&str>>().join(""))
        .collect();
    println!("{:?}", stuff);
    return 0;
}
