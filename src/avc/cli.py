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
    parser.add_argument('-n', '--output_name', help="Optional name for the output file (without extension).")

    # Parse the arguments
    args = parser.parse_args()

    try:
        input_path, output_dir = validate_paths(args.input, args.output_dir)
        
        output_name = args.output_name if args.output_name else None
        
        avc_file = AVCFile(input_path, output_dir, output_name)
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
