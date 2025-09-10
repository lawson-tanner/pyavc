import os
from .utils import reverse_str, encode_u32le, encode_u64le, encode_u32be, encode_str, conform_byte_string, generate_truncated_uuidv7, extra_padding, count_carriage_returns, swap_lf_cr, calculate_and_insert_counts, wrap_txt_file_line
from datetime import datetime
from .bytestrings import footer1, footer2, placeholder, byte_order_indicator, identifier1, identifier2, identifier3, creator_description_len_marker, bs1, bs2, bs3, bs4
from .docx_utils import convert_docx_to_lines

class AVCException(Exception):
        def __init__(self, message="An unexpected error occurred."):
            self.message = message
            super().__init__(self.message)
        
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
        self.creator_description = "pyavc v1.0.11"
    
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
        
        
        
        

class BTXTChunk():
    def __init__(self, uuid, txt_lines, font_size: int, font_name: str, script_bg_interface_or_white: bool, show_row_colors: bool, left_margin: int, text_width_px: int, show_frames: bool, interpolate_position: bool, show_all_takes: bool, show_line_numbers: bool, word_wrap: bool, hold_slates_onscreen: bool, take_color: int):
        self.txt_lines = txt_lines
        self.class_id = u'BTXT'

        self.num_char = 0
        self.num_lines = 0
        self.num_newlines = 0
        self.uuid = uuid
        self.footer1 = footer1
        self.footer2 = footer2
        self.font_size = font_size
        self.font_name = font_name.strip().encode('ascii')
        self.use_white_bg = script_bg_interface_or_white.to_bytes(1)
        if script_bg_interface_or_white:
            show_row_colors = False
        self.show_row_colors = show_row_colors.to_bytes(1)
        self.left_margin = left_margin.to_bytes(4, byteorder='little')
        self.word_wrap = word_wrap.to_bytes(1)
        
        if not word_wrap:
            text_width_px = False
       
        if text_width_px and not text_width_px >= 128:
            raise AVCException("Insufficient text width value: must be minimum of 128 pixels.")
        if text_width_px and not text_width_px <= 5120:
            raise AVCException("Exceeded maximum permissible text width of 5120px.")
        

        self.text_width_px = text_width_px.to_bytes(2, byteorder="little")
        self.show_frames = show_frames.to_bytes(1)
        self.interpolate_position = interpolate_position.to_bytes(1)
        self.show_all_takes = show_all_takes.to_bytes(1)
        self.show_line_numbers = show_line_numbers.to_bytes(1)
        self.hold_slates_onscreen = hold_slates_onscreen.to_bytes(1)
        self.take_color = take_color.to_bytes(1)

        
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

        # trimming 4 bytes off the end of bs3 - conform byte string with hex(font_size), 3
        font_size_byte = self.font_size.to_bytes(4, byteorder="little")

        data += font_size_byte
        
        # Add footer1
        data += conform_byte_string(footer1)
        
        # Add bs4 and 5 padding characters
        data += conform_byte_string(bs4, 5)
        
        # Add UUID
        data += conform_byte_string(self.uuid, 8)
        # Add footer2
        #data += conform_byte_string(footer2)

        data += self.take_color

        data += b'\x00'

        data += self.show_all_takes

        data += self.left_margin

        data += b"\x01\x01\x42"

        data += self.interpolate_position

        data += b"\x01\x02\x42"

        data += self.hold_slates_onscreen

        data += b"\x01\x03\x47"

        data += self.text_width_px

        data += b"\x00\x00\x01\x04\x42"

        data += self.word_wrap

        data += b"\x01\x05\x42"

        data += self.show_frames

        data += b"\x42"

        data += self.use_white_bg

        data += b"\x42"

        data += self.show_row_colors

        data += b"\x42"

        data += self.show_line_numbers

        data += b"\x01\x06\x4C"

        data += len(self.font_name).to_bytes(2, byteorder="little")

        data += self.font_name

        data += b"\x03"

        # End count of NUM CHAR C
        num_char_c_end = len(data)
        
        
        # Calculate and insert counts using the helper function
        calculate_and_insert_counts(data, num_char_a_start, num_char_a_end, num_char_a_idx)
        calculate_and_insert_counts(data, num_char_d_start, num_char_d_end, num_char_d_idx)
        calculate_and_insert_counts(data, num_char_c_start, num_char_c_end, num_char_c_idx)
        
        return data

    




class AVCFile:

    def __init__(
            self, 
            input_path, 
            output_dir, 
            output_file_name: str = None, 
            text_width: int = 80, 
            font_size: int = 12, 
            font_name: str = "Open Sans", 
            white_bg: bool = False, 
            show_row_colors: bool = True, 
            left_margin: int = 40, 
            text_width_px: int = 512,
            show_frames: bool = True, 
            interpolate_position: bool = False, 
            show_all_takes: bool = True, 
            show_line_numbers: bool = True, 
            word_wrap: bool = True, 
            hold_slates_onscreen: bool = False, 
            take_color: int = 1):
        
        self.name = output_file_name
        self.output_dir = output_dir
        self.full_path = None
        self.input_file = input_path
        self.txt_lines = None
        self.text_width = text_width
        self.uuid = generate_truncated_uuidv7()
        self.header = None
        self.btxt_chunk = None
        self.font_size = font_size
        self.font_name = font_name
        self.white_bg = white_bg
        self.show_row_colors = show_row_colors
        self.left_margin = left_margin
        self.text_width_px = text_width_px
        self.show_frames = show_frames
        self.interpolate_position = interpolate_position
        self.show_all_takes = show_all_takes
        self.show_line_numbers = show_line_numbers
        self.word_wrap = word_wrap
        self.hold_slates_onscreen = hold_slates_onscreen
        self.take_color = take_color

        
    def create(self):
        if self.input_file.lower().endswith('.txt'):
            # Read txt file - must be UTF-8
            with open(self.input_file, 'r', encoding='utf-8-sig') as txt:
                self.txt_lines = txt.readlines()
                new_txt_lines = []
                for line in self.txt_lines:
                    wrapped_txt = wrap_txt_file_line(line, self.text_width)
                    new_txt_lines.extend(wrapped_txt)  # Use extend to add all wrapped lines
                self.txt_lines = new_txt_lines
                
        
        elif self.input_file.lower().endswith('.docx'):
            self.txt_lines = convert_docx_to_lines(self.input_file, self.text_width)
    
        # Step 2: Determine the base name and enforce the 56-character limit
        if self.name is None:
            # Split the base name and the extension
            base_name, ext = os.path.splitext(os.path.basename(self.input_file))
        else:
            base_name = self.name
    
        # Trim any trailing whitespace from the base name
        base_name = base_name.rstrip()
    
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
        self.btxt_chunk = BTXTChunk(self.uuid, self.txt_lines, self.font_size, self.font_name, self.white_bg, self.show_row_colors, self.left_margin, self.text_width_px, self.show_frames, self.interpolate_position, self.show_all_takes, self.show_line_numbers, self.word_wrap, self.hold_slates_onscreen, self.take_color)
        btxt_data = self.btxt_chunk.create()
        
        output = header_data + btxt_data
        
        # Write data to file
        with open(self.full_path, 'wb') as avc:
            avc.write(output)
        
        print(f"AVC file created successfully at {self.full_path}")
        return self.full_path
        
 

