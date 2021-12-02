use std::error::Error;
use std::fs;

fn main() -> Result<(), Box<dyn Error>> {
    let input = read_input()?;
    let pos = navigate(&input);
    let traj = navigate2(&input);
    println!("Position {:?}, product {}", pos, pos.horizontal * pos.depth);
    println!(
        "Trajectory {:?}, product {}",
        traj,
        traj.pos.horizontal * traj.pos.depth
    );
    Ok(())
}

fn read_input() -> Result<String, Box<dyn Error>> {
    Ok(fs::read_to_string("inputs/02-dive")?)
}

fn navigate(cmds: &String) -> Position {
    let mut pos = Position::initial();

    for cmd in cmds.lines() {
        pos = pos.mv(cmd.to_string());
    }

    pos
}

fn navigate2(cmds: &String) -> Trajectory {
    let mut traj = Trajectory::initial();

    for cmd in cmds.lines() {
        traj = traj.mv(cmd.to_string());
    }

    traj
}

#[derive(Clone, Copy, Debug)]
struct Position {
    horizontal: i32,
    depth: i32,
}

impl Position {
    fn initial() -> Position {
        Position {
            horizontal: 0,
            depth: 0,
        }
    }

    /// Naive movement for part 1
    fn mv(&self, cmd: String) -> Position {
        let parts: Vec<&str> = cmd.split(' ').collect();
        let c = parts[0].chars().next().unwrap();
        let i: i32 = parts[1].parse().unwrap();

        if c == 'u' {
            Position {
                horizontal: self.horizontal,
                depth: self.depth - i,
            }
        } else if c == 'd' {
            Position {
                horizontal: self.horizontal,
                depth: self.depth + i,
            }
        } else {
            Position {
                horizontal: self.horizontal + i,
                depth: self.depth,
            }
        }
    }
}

#[derive(Debug)]
struct Trajectory {
    pos: Position,
    aim: i32,
}

impl Trajectory {
    fn initial() -> Trajectory {
        Trajectory {
            pos: Position::initial(),
            aim: 0,
        }
    }

    /// More complex movement based on aim, for part 2
    fn mv(&self, cmd: String) -> Trajectory {
        let parts: Vec<&str> = cmd.split(' ').collect();
        let c = parts[0].chars().next().unwrap();
        let i: i32 = parts[1].parse().unwrap();

        if c == 'u' {
            Trajectory {
                pos: self.pos,
                aim: self.aim - i,
            }
        } else if c == 'd' {
            Trajectory {
                pos: self.pos,
                aim: self.aim + i,
            }
        } else {
            Trajectory {
                pos: Position {
                    horizontal: self.pos.horizontal + i,
                    depth: self.pos.depth + self.aim * i,
                },
                aim: self.aim,
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use crate::*;

    static EXAMPLE: &str = r#"forward 5
down 5
forward 8
up 3
down 8
forward 2
"#;

    #[test]
    fn test_part_1() {
        let pos = navigate(&EXAMPLE.to_string());
        assert_eq!(pos.horizontal * pos.depth, 150);
    }

    #[test]
    fn test_part_2() {
        let traj = navigate2(&EXAMPLE.to_string());
        assert_eq!(traj.pos.horizontal * traj.pos.depth, 900);
    }
}
