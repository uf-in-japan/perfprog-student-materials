use std::vec::Vec;

fn main()
{
    let mut greeting = Vec::new();

    greeting.push(String::from("Hello, "));
    greeting.push(String::from("Rusty World!"));

    for element in greeting
    {
        print!("{}", element);
    }
    println!("");
}
