import struct, time, uuid


def generate_truncated_uuidv7():
    
    """
    Generate a truncated UUIDv7-like value consisting of a 48-bit timestamp and 16 bits of randomness.

    Returns:
        bytes: A 64-bit big-endian byte string representing the truncated UUIDv7.
    """
    
    # Generate a 48-bit timestamp (milliseconds since the Unix epoch)
    timestamp_ms = int(time.time() * 1000) & 0xFFFFFFFFFFFF  # Mask to 48 bits
    
    # Generate 16 bits of randomness
    random_bits = uuid.uuid4().int & 0xFFFF
    
    # Combine the timestamp and random bits
    combined_value = (timestamp_ms << 16) | random_bits  # 64-bit value
    
    # Convert to big-endian byte string
    truncated_uuidv7 = struct.pack('>Q', combined_value)
    
    return truncated_uuidv7

def count_carriage_returns(lines):
    """
    Count the number of carriage return characters (\x0D) in a list of strings.

    Args:
        lines (list of str): A list of text lines to check.

    Returns:
        int: The total number of \x0D characters found across all lines.
    """
    count_newlines = 0
    for line in lines:
        count_newlines += line.count('\x0D')
    return count_newlines
    
def swap_lf_cr(text):
    """
    Swap LF (\n) with CR (\r) in the given string.

    Args:
        text (str): The input string to process.

    Returns:
        str: The string with LF and CR swapped.
    """
    return text.replace('\n', '\r').replace('\r', '\n')
    

def calculate_and_insert_counts(data, start_marker, end_marker, placeholder_idx):
    """
    Calculates the count of bytes between start_marker and end_marker, 
    then inserts the count at the placeholder_idx in the data bytearray.
    
    Args:
    - data (bytearray): The bytearray containing the data.
    - start_marker (int): The starting index to begin counting.
    - end_marker (int): The ending index to stop counting.
    - placeholder_idx (int): The index where the calculated count should be inserted.
    """
    byte_count = end_marker - start_marker
    data[placeholder_idx:placeholder_idx+4] = encode_u32le(byte_count)
    




def reverse_str(fourcc):
    """
    Convert a FOURCC code to a 32-bit little-endian byte string.

    Args:
        fourcc (str): The FOURCC code (4 characters).

    Returns:
        bytes: The little-endian encoded FOURCC code.
    """
    if len(fourcc) != 4:
        raise ValueError("FOURCC must be exactly 4 characters long")

    # Convert the string to ASCII bytes and pack as a 32-bit integer
    fourcc_bytes = struct.pack("<I", struct.unpack(">I", fourcc.encode('ascii'))[0])

    return fourcc_bytes

def extra_padding(num_bytes, pad_byte=b'\x00'):
    """
    Generate padding bytes.

    Args:
        num_bytes (int): Number of padding bytes.
        pad_byte (bytes): The byte to use for padding.

    Returns:
        bytes: The padding bytes.
    """
    return pad_byte * num_bytes

def conform_byte_string(byte_string, padding_len=0, padding_byte=b'\x00'):
    """
    Convert a big-endian byte string to little-endian and add padding.

    Args:
        byte_string (bytes): The original byte string (big-endian).
        padding_len (int): The number of padding bytes to add.
        padding_byte (bytes): The byte to use for padding.

    Returns:
        bytes: The padded, little-endian byte string.
    """
    # Convert to little-endian by reversing the string
    little_endian_byte_string = byte_string[::-1]
    
    # Add the specified padding
    padded_byte_string = little_endian_byte_string + (padding_byte * padding_len)
    
    return padded_byte_string
    
def encode_str(value):
    """
    Encode a string to UTF-8 bytes.

    Args:
        value (str): The string to encode.

    Returns:
        bytes: The UTF-8 encoded string.
    """
    return value.encode('utf-8')


def encode_u32le(value):
    """
    Encode an integer as a little-endian unsigned 32-bit value.

    Args:
        value (int): The integer to encode.

    Returns:
        bytes: The 32-bit encoded integer.
    """
    return struct.pack("<I", value)


def encode_u64le(value):
    """
    Encode an integer as a little-endian unsigned 64-bit value.

    Args:
        value (int): The integer to encode.

    Returns:
        bytes: The 64-bit encoded integer.
    """
    if isinstance(value, bytes):
        # Convert the byte string to an integer
        value = int.from_bytes(value, byteorder='big')
    return struct.pack("<Q", value)


def encode_u32be(value):
    """
    Encode an integer as a big-endian unsigned 32-bit value.

    Args:
        value (int): The integer to encode.

    Returns:
        bytes: The 32-bit encoded integer.
    """
    return struct.pack(">I", value)

