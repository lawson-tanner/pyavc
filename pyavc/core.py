from file import AVCFile
import argparse, os

def txt_to_avc(txt_file, output_dir):
    if not os.path.exists(txt_file) or not txt_file.endswith('.txt'):
    	raise Exception()
    	
    elif not os.path.exists(output_dir):
    	raise Exception()
    
    avc = AVCFile(txt_file, output_dir)
    try:
        avc.create()
    except:
        print("There was an error!")