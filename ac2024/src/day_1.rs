use anyhow::{anyhow, Result};

use std::{
    collections::HashMap,
    io::{BufRead, BufReader, Read},
    iter::zip,
};

use crate::Day;

pub struct Day1 {
    left: Vec<i64>,
    right: Vec<i64>,
}

pub fn new<R: Read>(buf: BufReader<R>) -> Result<Day1> {
    let mut d = Day1 {
        left: Vec::new(),
        right: Vec::new(),
    };

    for line in buf.lines() {
        let l = line?;
        let parts = l.split_once("   ");
        match parts {
            Some((l, r)) => {
                d.left.push(l.parse()?);
                d.right.push(r.parse()?);
            }
            _ => return Err(anyhow!("No parts found")),
        }
    }

    d.left.sort();
    d.right.sort();

    Ok(d)
}

impl Day for Day1 {
    fn part_1(&self) -> Result<i64> {
        let r = zip(self.left.clone(), self.right.clone())
            .map(|(l, r)| (l - r).abs())
            .reduce(|sum, d| sum + d);

        match r {
            Some(r) => Ok(r),
            None => Err(anyhow!("no result")),
        }
    }

    fn part_2(&self) -> Result<i64> {
        let mut counts: HashMap<i64, i64> = HashMap::new();
        // Build map from value to count in right list
        self.right
            .iter()
            .for_each(|i| *counts.entry(*i).or_insert(0) += 1);
        // Sum number * count for each entry in the left list
        let r = self
            .left
            .iter()
            .map(|i| *i * *(counts.entry(*i).or_default()))
            .reduce(|sum, s| sum + s);

        match r {
            Some(r) => Ok(r),
            None => Err(anyhow!("no result")),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    static TEST_INPUT: &str = "3   4
4   3
2   5
1   3
3   9
3   3";

    fn setup() -> Result<Day1> {
        let r = BufReader::new(TEST_INPUT.as_bytes());
        new(r)
    }

    #[test]
    fn test_part_1() -> Result<()> {
        let r = setup()?;
        assert_eq!(r.part_1()?, 11);
        Ok(())
    }

    #[test]
    fn test_part_2() -> Result<()> {
        let r = setup()?;
        assert_eq!(r.part_2()?, 31);
        Ok(())
    }
}
