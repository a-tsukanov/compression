// Module containing functions to compress and decompress text using LZ77 algorithm

use std::collections::HashMap;
use std::iter::Enumerate;
use std::str::Chars;
use std::fmt;
use std::vec::Vec;


// Single element of compressed collection
#[derive(Debug)]
enum Node {
    Repetition {          // A piece of text already seen before.
        offset: usize,    // How far left is the piece of text.
        length: usize,    // How long it is.
    },
    Single {              // Just one character
        character: char,
    },
}


impl fmt::Display for Node {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Node::Single {character} => write!(f, "{}", character),
            Node::Repetition {offset, length} => write!(f, "[<-{}|{}]", offset, length),
        }
    }
}


fn main() {
    let text = "🌍🌎🔧🔧🚀 😎😎 Hi` 😎😎😎 дарова дарова aoahhzaoahhzaoahhz hhzaoahhz hhzaoahhz aoahhzaoahhzaoahhz hhzaoahhz hhzaoahhz \t ";

    let compressed = compress_lz77_to_vec(text);
    println!("{}", vec_to_str(&compressed));

    let decompressed = decompress_lz77(&compressed);
    println!("{}", decompressed);

    assert_eq!(text, &decompressed);
}


fn _get_utf8_slice(string: &str, start: usize, end: usize) -> &str {
    fn _get_idx(string: &str, idx: usize) -> usize {
        string.char_indices().map(|(i, _)| i).nth(idx).unwrap()
    }
    let start_byteindex = _get_idx(string, start);
    let end_byteindex
        = if end == string.chars().count() {string.len()} else { _get_idx(string, end)};

    &string[start_byteindex..end_byteindex]
}


/*
text: string slice to be compressed
returns: owned vector of nodes
*/
fn compress_lz77_to_vec(text: &str) -> Vec<Node> {
    let mut result = Vec::new();
    let mut enumerator: Enumerate<Chars> = text.chars().enumerate();

    while let Some((index, character)) = enumerator.next() {
        let seen = _get_utf8_slice(text, 0, index);
        let occurrences = _get_occurrences(&character, seen);

        if occurrences.is_empty() {
            result.push(Node::Single { character });
        }

        else {
            let (longest_position, longest_length)
                = _get_longest_repetition(text, occurrences, index);

            if longest_length == 1 {
                // we don't want a Repetition of length 1, it is inefficient
                result.push(Node::Single { character });
            }
            else {
                result.push(Node::Repetition {
                    offset: index - longest_position,
                    length: longest_length,
                });
            _skip_chars(&mut enumerator, &(longest_length - 1))
            }
        }

    }
    result
}


// returns a vector of character indices in the "seen" string slice
fn _get_occurrences(character: &char, seen: &str) -> Vec<usize> {
    seen.chars()
        .enumerate()
        .filter(|(_, c)| c == character)
        .map(|(i, _)| i)
        .collect()
}


// given a HashMap (position => length) returns a tuple of (position, length) with the biggest length
fn _get_longest_repetition(original_text: &str, occurrences: Vec<usize>, current_index: usize) -> (usize, usize) {

    // returns a HashMap (position => length) with lengths of the found repetitions
    fn _get_substr_mappings(original_text: &str, occurrences: Vec<usize>, current_index: usize) -> HashMap<usize, usize> {
        let mut position_to_length = HashMap::new();
        let seen = _get_utf8_slice(original_text, 0, current_index);

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

    let position_to_length = _get_substr_mappings(&original_text, occurrences, current_index);
    let mut map_vec: Vec<(&usize, &usize)> = position_to_length.iter().collect();
    map_vec.sort_by(|a, b| b.1.cmp(a.1));  // sort by .1 field (length) descending
    let (position, length) = map_vec[0];
    (position.clone(), length.clone())
}


fn _skip_chars(e: &mut Enumerate<Chars>, n: &usize) {
    for _ in 0..*n { e.next(); }
}



fn vec_to_str(nodes: &Vec<Node>) -> String {
    nodes.iter().map(|item| format!("{}", item)).collect()
}


// decompresses a borrow of a vector of Nodes to an owned String
fn decompress_lz77(nodes: &Vec<Node>) -> String {
    let mut result = String::new();
    let mut index = 0;
    for node in nodes {
        let piece_to_append = match *node {
            Node::Single {character} => {
                index += 1;
                character.to_string()
            },
            Node::Repetition {offset, length} => {
                let start_index = index - offset;
                let end_index = start_index + length;
                index += length;
                _get_utf8_slice(&result, start_index, end_index).to_string()
            },
        };
        result.push_str(&piece_to_append);
    }
    result
}