import os
from .utils import reverse_str, encode_u32le, encode_u64le, encode_u32be, encode_str, conform_byte_string, generate_truncated_uuidv7, extra_padding, count_carriage_returns, swap_lf_cr, calculate_and_insert_counts
from datetime import datetime
from .bytestrings import footer1, footer2, placeholder, byte_order_indicator, identifier1, identifier2, identifier3, creator_description_len_marker, bs1, bs2, bs3, bs4
from .docx_utils import convert_docx_to_lines

class AVCHeader:
    def __init__(self, uuid):
        self.byte_order_indicator = byte_order_indicator
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
        self.creator_description = "pyavc v1.0.1"
    
    def create(self):
        data = bytearray()
        
        # Byte order indicator
        data += self.byte_order_indicator
        # Magic word
        data += encode_str(self.magic)
        # fourcc1
        data += reverse_str(self.fourcc1)
        # identifier1
        data += conform_byte_string(self.identifier1)
        # AObjDoc
        data += encode_str(self.objdoc) 
        # identifier2
        data += conform_byte_string(self.identifier2)
        # Timestamp str
        data += encode_str(self.timestamp_str)
        # identifier3
        data += conform_byte_string(self.identifier3)
        # iiii
        data += self.iiii    
        # uuid
        data += encode_u64le(self.uuid)
        # fourcc2
        data += reverse_str(self.fourcc2)
        # fourcc3
        data += reverse_str(self.fourcc3)
        # creator_description_length
        data += conform_byte_string(self.creator_description_len_marker)
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
        
        # Reverse and add the class id
        data += reverse_str(self.class_id)
        
        # NUM CHAR A Index
        num_char_a_idx = len(data)  

        # NUM CHAR A Placeholder
        data += placeholder  
        
        # Start count of NUM CHAR A
        num_char_a_start = len(data)
        
        # Add bs1
        data += bs1
        
        # NUM CHAR D Index
        num_char_d_idx = len(data)  

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

        data += conform_byte_string(encoded_num_newlines, 4)
        
        # Start count of NUM CHAR B (Recursive)
        running_total = 0
        for line in self.txt_lines:
            line_num_char = len(line)
            running_total += line_num_char
            encoded = encode_u32be(running_total)
            data += conform_byte_string(encoded)
        
        
        # Add bs2
        data += conform_byte_string(bs2)
        
        # Stop count of NUM CHAR A 
        num_char_a_end = len(data)
        data[num_char_a_idx:num_char_a_idx+4] = encode_u32le(len(data) - num_char_a_start)

        # Add 'Scpt' string
        data += reverse_str('Scpt')
        
        # NUM CHAR C Index
        num_char_c_idx = len(data)

        # NUM CHAR C Placeholder
        data += placeholder
        
        # Start count of NUM CHAR C
        num_char_c_start = len(data)
        
        # Add bs3
        data += conform_byte_string(bs3)
        
        # Add footer1
        data += conform_byte_string(footer1)
        
        # Add bs4 and 5 padding characters
        data += conform_byte_string(bs4, 5)
        
        # Add UUID
        data += conform_byte_string(self.uuid, 8)
        # Add footer2
        data += conform_byte_string(footer2)
        
        # End count of NUM CHAR C
        num_char_c_end = len(data)
        
        
        # Calculate and insert counts using the helper function
        calculate_and_insert_counts(data, num_char_a_start, num_char_a_end, num_char_a_idx)
        calculate_and_insert_counts(data, num_char_d_start, num_char_d_end, num_char_d_idx)
        calculate_and_insert_counts(data, num_char_c_start, num_char_c_end, num_char_c_idx)
        
        return data

    




class AVCFile:
    def __init__(self, input_path, output_dir, output_file_name=None):
        self.name = output_file_name
        self.output_dir = output_dir
        self.full_path = None
        self.input_file = input_path
        self.txt_lines = None
        self.uuid = generate_truncated_uuidv7()
        self.header = None
        self.btxt_chunk = None

        
    def create(self):
        if self.input_file.lower().endswith('.txt'):
            # Read txt file
            with open(self.input_file, 'r') as txt:
                self.txt_lines = txt.readlines()
        
        elif self.input_file.lower().endswith('.docx'):
            self.txt_lines = convert_docx_to_lines(self.input_file)

        # Step 2: Determine the base name and enforce the 56-character limit
        if self.name is None:
            # Split the base name and the extension
            base_name, ext = os.path.splitext(os.path.basename(self.input_file))
        else:
            base_name = self.name

        # Ensure the base name doesn't exceed 56 characters
        base_name = base_name[:56] if len(base_name) > 56 else base_name

        # Step 3: Construct the initial full path
        full_path = os.path.join(self.output_dir, f"{base_name}.avc")

        # Step 4: Check if the file exists and append an incrementing number if necessary
        if os.path.exists(full_path):
            count = 1
            while True:
                suffix = f"({count})"
                # Calculate the maximum allowed length for the base name after appending the suffix
                max_base_length = 56 - len(suffix)
                # Truncate the base name if necessary
                truncated_base = base_name[:max_base_length] if len(base_name) > max_base_length else base_name
                # Construct the new file name with the suffix
                new_file_name = f"{truncated_base}{suffix}.avc"
                new_full_path = os.path.join(self.output_dir, new_file_name)
                # Check if this new path exists
                if not os.path.exists(new_full_path):
                    full_path = new_full_path
                    break  # Exit the loop once a unique name is found
                count += 1  # Increment the counter and try again

        # Step 5: Assign the final path to the instance variable
        self.full_path = full_path


        
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
        return self.full_path
        
 

