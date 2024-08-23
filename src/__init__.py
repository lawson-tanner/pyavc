from file import AVCFile
import argparse, os

def txt_to_avc(txt_file, output_dir):
    avc = AVCFile(txt_file, output_dir)
    try:
        avc.create()
    except:
        print("There was an error!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--txt-file", type=str, help="Absolute path to TXT file you want to convert. Accepts any pathlike object compatible with os.path")
    parser.add_argument("--output-dir", type=str, help="Absolute path to output directory. Output file names are based on input file names. Accepts any pathlike object compatible with os.path")
    
    args = parser.parse_args()

    if args:
        txt_file, output_dir = args
        txt_to_avc(txt_file, output_dir)
