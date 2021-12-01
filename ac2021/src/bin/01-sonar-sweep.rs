use std::error::Error;
use std::fs;

use itertools::izip;

fn main() -> Result<(), Box<dyn Error>> {
    let input = read_input()?;
    let depths = parse_input(input);
    let c = count_increases(&depths);
    let s = count_sliding(&depths);

    println!("Part 1 (increases): {}", c);
    println!("Part 2 (sliding): {}", s);

    Ok(())
}

fn read_input() -> Result<String, Box<dyn Error>> {
    Ok(fs::read_to_string("inputs/01-sonar-sweep")?)
}

fn parse_input(i: String) -> Vec<i32> {
    i.lines().map(|l| l.parse().unwrap()).collect()
}

fn count_increases(depths: &Vec<i32>) -> i32 {
    let mut count = 0;
    let mut last = None;

    for i in depths {
        if let Some(prev) = last {
            if i > prev {
                count += 1;
            }
        }

        last = Some(i);
    }

    count
}

fn count_sliding(depths: &Vec<i32>) -> i32 {
    let mut count = 0;
    let mut last: Option<(&i32, &i32, &i32)> = None;

    let windows = izip!(depths[0..].iter(), depths[1..].iter(), depths[2..].iter());

    for w in windows {
        if let Some(prev) = last {
            if w.0 + w.1 + w.2 > prev.0 + prev.1 + prev.2 {
                count += 1;
            }
        }

        last = Some(w);
    }

    count
}

#[cfg(test)]
mod tests {
    use crate::*;

    static EXAMPLE: &str = r#"199
200
208
210
200
207
240
269
260
263
"#;

    #[test]
    fn test_part_1() {
        assert_eq!(count_increases(&parse_input(String::from(EXAMPLE))), 7);
    }

    #[test]
    fn test_part_2() {
        assert_eq!(count_sliding(&parse_input(String::from(EXAMPLE))), 5);
    }
}
