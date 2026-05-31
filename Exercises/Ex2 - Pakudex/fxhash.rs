 // Hash a sequence of bytes (any length)

#[inline]
pub fn hash_bytes(bytes: &[u8]) -> u64 {
    let rotate_left = |value: u64, n: u8| (value << n) | (value << (64 - n));
    let add_to_hash = |hash: u64, i: u64| (rotate_left(hash, 5) ^ i).wrapping_mul(0x517cc1b727220a95); // WAT?...
    let bytes_to_u64 = |source: [u8; 8]| (u64::from_le_bytes(source));

    let mut hash: u64 = 0; // Our persistent hash value (across 8-bytes blocks)
    let mut index: usize = 0;    // Current index within the byte array
    let mut temp: [u8; 8] = [0; 8];

    // First, iterate and hash the complete 8-byte blocks.
    while index + 8 < bytes.len() {
        temp[..].copy_from_slice(&bytes[index..(index+8)]); // Copy the next 8 bytes into the temp array
        hash = add_to_hash(hash, bytes_to_u64(temp)); // Hash this 8-byte block
        index += 8; // increment the index
    }

    // Finally, fill in zeros and hash any remaining bytes.
    temp = [0; 8];
    temp[..bytes.len()].copy_from_slice(&bytes[index..]);
    add_to_hash(hash, bytes_to_u64(temp))
}

