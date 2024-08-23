import struct, os, time, uuid, binascii
from utils import reverse_str, encode_u8, encode_u16le, encode_u32le, encode_u64le, encode_u32be, encode_str, conform_byte_string, generate_truncated_uuidv7, extra_padding, count_carriage_returns, swap_lf_cr, calculate_and_insert_counts
from datetime import datetime
from bytestrings import footer1, footer2, placeholder, identifier1, identifier2, identifier3, creator_description_len_marker, bs1, bs2, bs3

class AVCHeader:
    def __init__(self, uuid):
        self.byte_order_indicator = b'\x06\x00' # Write directly to file
        self.magic = 'Domain'
        self.fourcc1 = 'OBJD'
        self.identifier1 = identifier1
        self.objdoc = 'AObjDoc'
        self.identifier2 = identifier2
        self.timestamp_str = datetime.now().strftime(u'%Y/%m/%d %H:%M:%S')
        self.identifier3 = identifier3
        self.iiii = b'IIII'
        self.uuid = uuid
        self.fourcc2 = u'ATsc'
        self.fourcc3 = u'ATve' 
        
        self.creator_description_len_marker = creator_description_len_marker
        self.creator_description = "pyavc v1.1"
    
    def create(self):
        data = bytearray()
        
        # Byte order indicator
        data += self.byte_order_indicator
        
        # Magic word
        data += encode_str(self.magic)
        
        # fourcc1
        
        data += reverse_str(self.fourcc1)
        
        # identifier1
        data += conform_byte_string(self.identifier1, 0)
        
        # AObjDoc
        data += encode_str(self.objdoc)
        
        # identifier2
        data += conform_byte_string(self.identifier2, 0)
        # Timestamp str
        data += encode_str(self.timestamp_str)
        # identifier3
        data += conform_byte_string(self.identifier3, 0)
        # iiii
        data += self.iiii
        
        # uuid
        data += encode_u64le(self.uuid)
        # fourcc2
        data += reverse_str(self.fourcc2)
        # fourcc3
        data += reverse_str(self.fourcc3)
        # creator_description_length
        data += conform_byte_string(self.creator_description_len_marker, 0)
        # Creator description + pad until 0x00000076 (inclusive)
        # Creator description + pad until 30 bytes
        encoded_desc = encode_str(self.creator_description)
        if len(encoded_desc) > 30:
            data += encoded_desc[:30]  # Truncate to 30 bytes
        else:
            to_pad = 30 - len(encoded_desc)
            data += encoded_desc
            data += b'\x20' * to_pad  # Pad with spaces until 30 bytes
        
        # Add extra padding
        data += extra_padding(16)
        
        return data
        
        
        
        

class BTXTChunk:
    def __init__(self, uuid, txt_lines):
        self.txt_lines = txt_lines
        self.class_id = u'BTXT'
        self.num_char = 0
        self.num_lines = 0
        self.num_newlines = 0
        self.uuid = uuid
        self.footer1 = footer1
        self.footer2 = footer2

        
    def create(self):
        data = bytearray()
        formatted_lines = []
        
        # Reverse and add the FOURCC code 
        data += reverse_str(self.class_id)  # Adds 'BXTT' in bytes
        
        # NUM CHAR A Index
        num_char_a_idx = len(data)  # Save index to update later

        # NUM CHAR A Placeholder
        data += placeholder  
        
        # Start count of NUM CHAR A
        num_char_a_start = len(data)
        
        
        # Add bs1
        data += bs1
        
        # NUM CHAR D Index
        num_char_d_idx = len(data)  # Save index to update later

        # NUM CHAR D Placeholder
        data += placeholder
        
        # Start count of NUM CHAR D
        num_char_d_start = len(data)
        
        
        # Count the number of characters and insert text content
        for line in self.txt_lines:
            stripped_line = line.rstrip('\n').rstrip('\r')
            swapped = swap_lf_cr(stripped_line)
            swapped += '\r'
            formatted_lines.append(swapped)
            encoded_line = encode_str(swapped)
            data += encoded_line
        
        
        # Stop count of NUM CHAR D
        num_char_d_end = len(data)
        data[num_char_d_idx:num_char_d_idx+4] = encode_u32le(len(data) - num_char_d_start)
        
        # Insert num newline chars in text content
        self.num_newlines = count_carriage_returns(formatted_lines)
        encoded_num_newlines = encode_u32be(self.num_newlines)
        
        # Padding \x00 * 4
        data += conform_byte_string(encoded_num_newlines, 4)
        
        # Start count of NUM CHAR B (Recursive)
        running_total = 0
        for line in self.txt_lines:
            line_num_char = len(line)
            running_total += line_num_char
            encoded = encode_u32be(running_total)
            data += conform_byte_string(encoded, 0)
        
        # Stop count of NUM CHAR B (Recursive)
        num_char_b_recursive_end = len(data)
        
        
        # Add bs2
        data += conform_byte_string(bs2, 0)
        
        # Stop count of NUM CHAR A 
        num_char_a_end = len(data)
        data[num_char_a_idx:num_char_a_idx+4] = encode_u32le(len(data) - num_char_a_start)
        
        # Add 'Scpt' string
        data += reverse_str('Scpt')
        
        # NUM CHAR C Placeholder
        num_char_c_idx = len(data)  # Save index to update later
        data += placeholder
        
        # Start count of NUM CHAR C
        num_char_c_start = len(data)
        
        
        # Add bs3
        data += bs3
        
        # Add footer1
        footer1_to_add = conform_byte_string(self.footer1, 0)
        data += footer1_to_add
        
        # Add padding and finalize the remaining part
        data += conform_byte_string(b'\x06', 5)
        
        # Add UUID and footers
        uuid_to_add = conform_byte_string(self.uuid, 8)
        data += uuid_to_add
        
        footer2_to_add = conform_byte_string(self.footer2, 0)
        data += footer2_to_add
        
        # End of NUM CHAR C
        num_char_c_end = len(data)
        
        
        # Calculate and insert counts using the helper function
        calculate_and_insert_counts(data, num_char_a_start, num_char_a_end, num_char_a_idx)
        calculate_and_insert_counts(data, num_char_d_start, num_char_d_end, num_char_d_idx)
        calculate_and_insert_counts(data, num_char_c_start, num_char_c_end, num_char_c_idx)
        
        return data

    




class AVCFile:
    def __init__(self, txt_path, output_dir):
        self.name = ""
        self.output_dir = output_dir
        self.full_path = None
        self.txt_file = txt_path
        self.txt_lines = None
        self.uuid = generate_truncated_uuidv7()
        self.header = None
        self.btxt_chunk = None

        
    def create(self):
        # Read txt file
        with open(self.txt_file, 'r') as txt:
        	self.txt_lines = txt.readlines()
        
        # Name output file based on input file, truncate to max length
        self.name = os.path.basename(self.txt_file).rstrip('.txt')
        if len(self.name) > 56:
            self.name = self.name[:56]
        self.full_path = os.path.join(self.output_dir, f"{self.name}.avc")
        
        # Generate header
        self.header = AVCHeader(self.uuid)
        header_data = self.header.create()
        # Generate BTXT chunk
        self.btxt_chunk = BTXTChunk(self.uuid, self.txt_lines)
        btxt_data = self.btxt_chunk.create()
        
        output = header_data + btxt_data
        
        # Write data to file
        with open(self.full_path, 'wb') as avc:
            avc.write(output)
        print(f"AVC file created successfully at {self.full_path}")
 

