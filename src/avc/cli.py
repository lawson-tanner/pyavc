import sys
import argparse
import os
from .file import AVCFile

def replace_smart_quotes(s):
    smart_quotes = {
        '“': '"',  # Left double quotation mark
        '”': '"',  # Right double quotation mark
        '‘': "'",  # Left single quotation mark
        '’': "'",  # Right single quotation mark
    }
    for smart, straight in smart_quotes.items():
        s = s.replace(smart, straight)
    return s

def fix_split_arguments(args):
    fixed_args = []
    temp_arg = []
    inside_quotes = False

    for arg in args:
        if arg.startswith('"') or arg.startswith("'"):
            inside_quotes = True
            temp_arg.append(arg.lstrip('"').lstrip("'"))
        elif arg.endswith('"') or arg.endswith("'"):
            inside_quotes = False
            temp_arg.append(arg.rstrip('"').rstrip("'"))
            fixed_args.append(" ".join(temp_arg))
            temp_arg = []
        elif inside_quotes:
            temp_arg.append(arg)
        else:
            fixed_args.append(arg)
    
    if temp_arg:  # Append any remaining arguments
        fixed_args.append(" ".join(temp_arg))
    
    # Remove any trailing or leading quotes from fixed_args
    fixed_args = [arg.strip('"').strip("'") for arg in fixed_args]

    return fixed_args


def ensure_absolute_path(path):
    if path.startswith("Users/"):
        path = "/" + path
    return os.path.abspath(path)

def validate_paths(filepath, output_dir):
    filepath = ensure_absolute_path(filepath)
    output_dir = ensure_absolute_path(output_dir)

    #print(f"Resolved input path: {filepath}")
    #print(f"Resolved output directory: {output_dir}")

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"The input file '{filepath}' does not exist.")
    
    if not (filepath.lower().endswith('.txt') or filepath.lower().endswith('.docx')):
        raise ValueError(f"The input file '{filepath}' must be a .txt or .docx file.")
    
    if not os.path.exists(output_dir):
        raise NotADirectoryError(f"The output directory '{output_dir}' does not exist or is not a directory.")

    return filepath, output_dir

def main():

    sys.argv = [replace_smart_quotes(arg) for arg in sys.argv]
    sys.argv = fix_split_arguments(sys.argv)
    
    #print(f"Processed arguments: {sys.argv}")

    # Create the parser
    parser = argparse.ArgumentParser(description="Process a DOCX or TXT file into the desired output format.")

    # Add arguments
    parser.add_argument('-i', '--input', required=True, help="Path to the input DOCX or TXT file.")
    parser.add_argument('-o', '--output_dir', required=True, help="Path to the output directory.")
    parser.add_argument('-n', '--output_name', help="Str: Optional name for the output file (without extension).")
    parser.add_argument('-t', '--text_width', help="Int: Optional max chars before line break is inserted")
    parser.add_argument('-f', '--font_size', help="Int: Optional font size.")
    parser.add_argument('-fn', '--font_name', help="Str: Optional font name")
    parser.add_argument('-wbg', '--white_bg', help="Bool: Optionally use white background if True or use system settings if False")
    parser.add_argument('-r', '--show_row_colors', help="Bool: Show alternating colors demarcating rows")
    parser.add_argument('-ml', '--margin_left', help="Int: Optional left margin, in pixels.")
    parser.add_argument('-tpx', '--text_width_px', help="Int: Optional text width, in px. This differs from the -text_width argument in that it only affects display and will not add LR/CF.")
    parser.add_argument('-sf', '--show_frames', help="Bool: Display mini thumbnail on slate.")
    parser.add_argument('-ip', '--interpolate_position', help="Bool: Optional: Allow manual sync marks")
    parser.add_argument('-a', '--show_all_takes', help="Bool: Optionally show all takes.")
    parser.add_argument('-ln', '--show_line_numbers', help="Bool: Optionally show line numbers on the left side.")
    parser.add_argument('-ww', '--word_wrap', help="Bool: Optionally wrap lines (visually only) where they extend past the established margins")
    parser.add_argument('-hs', '--hold_slates_onscreen', help="Bool: Optionally display slate info in the record monitor")
    parser.add_argument('-tk', '--take_color', help="Int: Optionally specify take color as a number between 1 and 22 (see README for the color palette)")
    # Parse the arguments
    args = parser.parse_args()

    try:
        input_path, output_dir = validate_paths(args.input, args.output_dir)
        
        output_name = args.output_name if args.output_name else None
        text_width = args.text_width if args.text_width else 80
        font_size = args.font_size if args.font_size else 12
        font_name = args.font_name if args.font_name else "Open Sans"
        white_bg = args.white_bg if args.white_bg != None else False
        show_row_colors = args.show_row_colors if args.show_row_colors != None else True
        margin_left = args.margin_left if args.margin_left else 40
        text_width_px = args.text_width_px if args.text_width_px else 512
        show_frames = args.show_frames if args.show_frames else True
        interpolate_position = args.interpolate_position if args.interpolate_position != None else False
        show_all_takes = args.show_all_takes if args.show_all_takes != None else True
        show_line_numbers = args.show_line_numbers if args.show_line_numbers != None else True
        word_wrap = args.word_wrap if args.word_wrap != None else True
        hold_slates_onscreen = args.hold_slates_onscreen if args.hold_slates_onscreen != None else False
        take_color = args.take_color if args.take_color else 1
        avc_file = AVCFile(input_path, output_dir, output_name, text_width, font_size, font_name, white_bg, show_row_colors, margin_left, text_width_px, show_frames, interpolate_position, show_all_takes, show_line_numbers, word_wrap, hold_slates_onscreen, take_color)
        output_path = avc_file.create()
        
        #print(f"Successfully processed '{input_path}' to '{output_path}'.")

    except FileNotFoundError as fnf_error:
        print(f"Error: {fnf_error}")
        sys.exit(1)
    except ValueError as ve:
        print(f"Error: {ve}")
        sys.exit(1)
    except NotADirectoryError as nde:
        print(f"Error: {nde}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
