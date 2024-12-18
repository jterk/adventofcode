use anyhow::{anyhow, Result};

use std::{
    collections::HashMap,
    env,
    fs::{self, File},
    io::{BufRead, BufReader},
};

mod day_1;
mod day_2;
mod day_3;

trait Day {
    fn part_1(&self) -> Result<i64>;
    fn part_2(&self) -> Result<i64>;
}

fn load_dot_env() -> Result<HashMap<String, String>> {
    let file = File::open(".env")?;

    let mut env = HashMap::new();
    let reader = BufReader::new(file);

    for line in reader.lines() {
        let s = line?;
        let words: Vec<&str> = s.split('=').collect();

        if words.len() != 2 {
            return Err(anyhow!("Malformed env line {}", s));
        }

        env.insert(words[0].to_string(), words[1].to_string());
    }

    Ok(env)
}

fn get_day(day: u8, buf: BufReader<File>) -> Result<Box<dyn Day>> {
    match day {
        1 => Ok(Box::new(day_1::new(buf)?)),
        2 => Ok(Box::new(day_2::new(buf)?)),
        3 => Ok(Box::new(day_3::new(buf)?)),
        _ => Err(anyhow!("Unknown day {}", day)),
    }
}

fn get_input(env: HashMap<String, String>, day: u8) -> Result<BufReader<File>> {
    fs::create_dir_all("inputs")?;
    let filename = format!("inputs/{}", day);
    let f = File::open(filename.clone());

    match f {
        Ok(f) => Ok(BufReader::new(f)),
        _ => {
            let url = format!("https://adventofcode.com/2024/day/{}/input", day);
            let client = reqwest::blocking::Client::new();
            let res = client
                .get(url)
                .header(
                    "Cookie",
                    format!(
                        "session={}",
                        env.get("SESSION_COOKIE").expect("SESSION_COOKIE not set")
                    ),
                )
                .send()?;
            fs::write(filename.clone(), res.text()?)?;
            Ok(BufReader::new(File::open(filename)?))
        }
    }
}

fn main() -> Result<()> {
    let env = load_dot_env()?;
    let args: Vec<String> = env::args().collect();
    let day_arg = args[1].parse::<u8>()?;
    let input = get_input(env, day_arg)?;
    let day = get_day(day_arg, input)?;

    println!("Computing results for day {}...", day_arg);

    let results = vec![day.part_1(), day.part_2()];

    results.iter().enumerate().for_each(|(i, r)| match r {
        Err(e) => println!("Part {} failed: {}", i + 1, e),
        Ok(r) => println!("Part {} result: {}", i + 1, r),
    });

    Ok(())
}
