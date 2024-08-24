from .file import AVCFile
import os

def convert(filepath, output_dir, output_name=None):
    if not os.path.exists(filepath):
            raise FileNotFoundError(f"The input file '{filepath}' does not exist.")
        
    if not (filepath.lower().endswith('.txt') or filepath.lower().endswith('.docx')):
        raise ValueError(f"The input file '{filepath}' must be a .txt or .docx file.")
        
        # Check if the output directory exists
    if not os.path.exists(output_dir):
        raise NotADirectoryError(f"The output directory '{output_dir}' does not exist or is not a directory.")
        
    avc = AVCFile(filepath, output_dir, output_name)
    try:
        avc.create()

    except:
        print("There was an error!")
