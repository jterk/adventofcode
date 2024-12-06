use std::io::{BufReader, Read};

use crate::Day;

pub struct Day3 {}

pub fn new<R: Read>(_buf: BufReader<R>) -> Day3 {
    Day3 {}
}

impl Day for Day3 {
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

    static TEST_INPUT: &str = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))";

    fn setup() -> Day3 {
        let r = BufReader::new(TEST_INPUT.as_bytes());
        new(r)
    }

    #[test]
    fn test_part_1() {
        let r = setup();
        assert_eq!(r.part_1(), Ok(161));
    }

    #[test]
    fn test_part_2() {
        let r = setup();
        assert_eq!(r.part_2(), Ok(-1));
    }
}
