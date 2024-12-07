use anyhow::{anyhow, bail, Result};
use regex::Regex;
use std::io::{BufRead, BufReader, Read};

use crate::Day;

pub struct Day3 {
    lines: Vec<String>,
}

pub fn new<R: Read>(buf: BufReader<R>) -> Result<Day3> {
    Ok(Day3 {
        lines: buf.lines().map(|l| l.unwrap_or("".to_string())).collect(),
    })
}

impl Day for Day3 {
    fn part_1(&self) -> Result<i64> {
        // mul(A,B)
        let re = Regex::new(r"mul\(([0-9]+),([0-9]+)\)")?;
        self
            .lines
            .iter()
            .map(|l| {
                re.captures_iter(l)
                    .map(|c| c.extract::<2>())
                    .map(|(_, cs)| cs[0].parse::<i64>().unwrap() * cs[1].parse::<i64>().unwrap())
                    .reduce(|s, v| s + v)
            })
            .map(|v| v.unwrap_or(0))
            .reduce(|s, v| s + v)
            .ok_or(anyhow!("failed to compute"))
    }

    fn part_2(&self) -> Result<i64> {
        bail!("Unimplemented")
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
