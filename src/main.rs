use std::collections::HashMap;

#[derive(Debug)]
enum Node {
    Repetition {
        character: char,
        offset: usize,
        length: usize,
    },
    Single {
        character: char,
    },
}

fn main() {
    println!("{:?}", text_to_nodes("aaaabrtyab"));
}

fn text_to_nodes(text: &str) -> Vec<Node> {
    let mut result = Vec::new();
    let mut enumerator = text.chars().enumerate();
    while let Some((index, character)) = enumerator.next() {
        let seen = &text[..index];
        let occurrences = get_occurrences(&character, seen);
        if occurrences.is_empty() {
            result.push(Node::Single { character });
        }
        else {
            let position_to_length: HashMap<_, _> = get_substr_mappings(text, occurrences, index);
            let mut map_vec: Vec<(&usize, &usize)> = position_to_length.iter().collect();
            map_vec.sort_by(|a, b| b.1.cmp(a.1));
            let (longest_position, longest_length) = map_vec[0];
            println!("{:?}", (longest_position, longest_length));
            if *longest_length == 1 {
                result.push(Node::Single { character });
            }
            else {
                result.push(Node::Repetition {
                    character,
                    offset: index - *longest_position,
                    length: *longest_length,
                });
                for _ in 0..(*longest_length - 1) {
                    enumerator.next();
                }
            }
        }

    }
    result
}

fn get_occurrences(character: &char, seen: &str) -> Vec<usize> {
    seen.chars()
        .enumerate()
        .filter(|(_, c)| c == character)
        .map(|(i, _)| i)
        .collect()
}

fn get_substr_mappings(original_text: &str, occurrences: Vec<usize>, current_index: usize) -> HashMap<usize, usize> {
    let mut position_to_length = HashMap::new();
    let seen = &original_text[..current_index];

    for position in occurrences {
        let mut length = 0;
        loop {
            let current_from_seen = seen.chars().nth(position + length);
            let current_from_original = original_text.chars().nth(current_index + length);
            match (current_from_seen, current_from_original) {
                (Some(c), Some(c2)) if c == c2 => {
                    length += 1;
                },
                _ => {
                    position_to_length.insert(position, length);
                    break;
                },
            };
        };
    }
    position_to_length
}