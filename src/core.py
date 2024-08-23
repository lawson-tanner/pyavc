from file import AVCFile
import os

def convert(filepath: os.Path, output_dir: os.Path, output_name=None):
    if not os.path.exists(filepath) or not filepath.lower().endswith('.txt') or not filepath.lower.endswith('.docx'):
        raise Exception()
    	
    elif not os.path.exists(output_dir):
        raise Exception()
    
    avc = AVCFile(filepath, output_dir, output_name)
    try:
        avc.create()

    except:
        print("There was an error!")
