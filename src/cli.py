# src/cli.py

import argparse
import os
import sys
from file import AVCFile

def main():
    # Create the parser
    parser = argparse.ArgumentParser(description="Process a DOCX or TXT file into the desired output format.")

    # Add arguments
    parser.add_argument('-i', '--input', required=True, help="Path to the input DOCX or TXT file.")
    parser.add_argument('-o', '--output_dir', required=True, help="Path to the output directory.")
    parser.add_argument('-n', '--output_name', help="Optional name for the output file (without extension).")

    # Parse the arguments
    args = parser.parse_args()

    # Validate input path
    input_path = args.input
    if not os.path.isfile(input_path):
        print(f"Error: The input file '{input_path}' does not exist.")
        sys.exit(1)

    # Validate file type
    if not input_path.lower().endswith(('.txt', '.docx')):
        print("Error: The input file must be a TXT or DOCX file.")
        sys.exit(1)

    # Validate output directory
    output_dir = args.output_dir
    if not os.path.isdir(output_dir):
        print(f"Error: The output directory '{output_dir}' does not exist.")
        sys.exit(1)

    # Determine the output file name
    if args.output_name:
        output_name = args.output_name
    else:
        output_name = os.path.splitext(os.path.basename(input_path))[0]  # Use input file name without extension

    # Determine the output file path
    output_path = os.path.join(output_dir, output_name)

    try:
        avc_file = AVCFile(input_path, output_dir, output_name)
        avc_file.create()
    except:
        print("Error: Unsupported file type.")
        sys.exit(1)

    print(f"Successfully processed '{input_path}' to '{output_path}'.")

if __name__ == '__main__':
    main()
