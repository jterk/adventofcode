use anyhow::Result;

use std::{
    cmp::{max, Ordering},
    io::{BufRead, BufReader, Read},
};

use crate::Day;

pub struct Day2 {
    reports: Vec<String>,
}

pub fn new<R: Read>(buf: BufReader<R>) -> Result<Day2> {
    Ok(Day2 {
        reports: buf.lines().map(|lr| lr.unwrap_or("".to_string())).collect(),
    })
}

#[derive(Clone, Copy, PartialEq)]
enum Order {
    Asc,
    Desc,
    Unknown,
}

fn to_order(l: i64, r: i64) -> Order {
    match l.cmp(&r) {
        Ordering::Greater => Order::Desc,
        Ordering::Less => Order::Asc,
        Ordering::Equal => Order::Unknown,
    }
}

fn is_safe(line: &str, dampen: bool) -> bool {
    let report: Vec<i64> = line.split(' ').map(|s| s.parse().unwrap()).collect();
    is_safe_inner(&report, dampen)
}

fn is_safe_inner(report: &[i64], dampen: bool) -> bool {
    let mut order = Order::Unknown;

    for (i, val) in report.iter().enumerate() {
        if i == 0 {
            order = to_order(report[i], report[i + 1]);
        } else {
            let delta = (report[i - 1] - val).abs();
            let new_order = to_order(report[i - 1], *val);

            if !(1..=3).contains(&delta) || order != new_order {
                if dampen {
                    let mut candidates = Vec::new();
                    let idx = i as i64;

                    for r in max(0, idx - 2)..idx + 1 {
                        let mut candidate = report.to_owned();
                        candidate.remove(r as usize);
                        candidates.push(candidate);
                    }

                    return candidates.iter().any(|c| is_safe_inner(c, false));
                } else {
                    return false;
                }
            }
        }
    }

    true
}

impl Day for Day2 {
    fn part_1(&self) -> Result<i64> {
        Ok(self.reports.iter().fold(
            0,
            |count, s| if is_safe(s, false) { count + 1 } else { count },
        ))
    }

    fn part_2(&self) -> Result<i64> {
        Ok(self.reports.iter().fold(
            0,
            |count, s| if is_safe(s, true) { count + 1 } else { count },
        ))
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
1 3 6 7 9
7 10 8 10 11
29 28 27 25 26 25 22 20
48 46 47 49 51 54 56
1 1 2 3 4 5
1 2 3 4 5 5
5 1 2 3 4 5
1 4 3 2 1
1 6 7 8 9
1 2 3 4 3
9 8 7 6 7";

    fn setup() -> Result<Day2> {
        let r = BufReader::new(TEST_INPUT.as_bytes());
        new(r)
    }

    #[test]
    fn test_part_1() -> Result<()> {
        let r = setup()?;
        assert_eq!(r.part_1()?, 2);
        Ok(())
    }

    #[test]
    fn test_part_2() -> Result<()> {
        let r = setup()?;
        assert_eq!(r.part_2()?, 14);
        Ok(())
    }
}
