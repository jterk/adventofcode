use anyhow::{anyhow, Result};
use std::io::{BufReader, Read};

use crate::Day;

pub struct Day3 {}

pub fn new<R: Read>(_buf: BufReader<R>) -> Result<Day3> {
    Ok(Day3 {})
}

impl Day for Day3 {
    fn part_1(&self) -> Result<i64> {
        Err(anyhow!("Unimplemented"))
    }

    fn part_2(&self) -> Result<i64> {
        Err(anyhow!("Unimplemented"))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    static TEST_INPUT: &str =
        "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))";

    fn setup() -> Result<Day3> {
        let r = BufReader::new(TEST_INPUT.as_bytes());
        new(r)
    }

    #[test]
    fn test_part_1() -> Result<()> {
        let r = setup()?;
        assert_eq!(r.part_1()?, 161);
        Ok(())
    }

    #[test]
    fn test_part_2() -> Result<()> {
        let r = setup()?;
        assert_eq!(r.part_2()?, -1);
        Ok(())
    }
}
