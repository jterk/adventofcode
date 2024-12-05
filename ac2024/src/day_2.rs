use std::io::{BufReader, Read};

use crate::Day;

pub struct Day2 {
}

pub fn new<R: Read>(_buf: BufReader<R>) -> Day2 {
    Day2 {}
}

impl Day for Day2 {
    fn part_1(&self) -> Result<i64, String> {
        Err("Unimplemented".to_string())
    }

    fn part_2(&self) -> Result<i64, String> {
        Err("Unimplemented".to_string())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    static TEST_INPUT: &str = "7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9";

    fn setup() -> Day2 {
        let r = BufReader::new(TEST_INPUT.as_bytes());
        new(r)
    }

    #[test]
    fn test_part_1() {
        let r = setup();
        assert_eq!(r.part_1(), Ok(2));
    }

    #[test]
    fn test_part_2() {
        let r = setup();
        assert_eq!(r.part_2(), Ok(-1));
    }
}

