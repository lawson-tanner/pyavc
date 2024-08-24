# pyavc

`pyavc` is a Python library that allows you to convert DOCX or TXT files into Avid Script (.avc) files. It can be used both as a command-line tool and as a library within your Python scripts.

This project is not affiliated with Avid or Avid Media Composer, it is simply an open source helper library to make fellow AEs' lives a bit easier.

## Installation

To install `pyavc`, you can use `pip3`:

```bash
pip3 install pyavc
```

## Usage

### As a Python Library

The main (and only) method provided is `convert`. It allows you to convert a DOCX or TXT file and save the result in a specified output directory.

```python
convert(filepath, output_dir, output_name=None)
```

#### Parameters

- **`filepath`** (`os.Path`): The path to the input DOCX or TXT file.
- **`output_dir`** (`os.Path`): The path to the output directory where the converted file will be saved.
- **`output_name`** (`str`, optional): The name of the output file (without extension). If not provided, the output file will be named based on the input file name.

#### Example Usage

```python
import pyavc as avc

# Convert a TXT file and save the output
avc.convert('/path/to/input.txt', '/path/to/output/dir')

# Convert a DOCX file and specify a custom output name
avc.convert('/path/to/input.docx', '/path/to/output/dir', output_name='custom_name')
```

### Command-Line Usage

`pyavc` can also be used from the command line to quickly convert files.

#### Syntax

```bash
pyavc -i <path-to-input-file> -o <path-to-output-dir> [-n <output-name>]
```

#### Parameters

- **`-i, --input`**: Path to the input DOCX or TXT file.
- **`-o, --output_dir`**: Path to the output directory where the converted file will be saved.
- **`-n, --output_name`**: (Optional) Name of the output file (without extension). If not provided, the output file will be named based on the input file name.

#### Example Commands

```bash
# Convert a TXT file and save the output
pyavc -i /path/to/input.txt -o /path/to/output/dir

# Convert a DOCX file and specify a custom output name
pyavc -i /path/to/input.docx -o /path/to/output/dir -n custom_name
```

## License

This project is licensed under the GPL 3.0 License. See the [LICENSE](LICENSE) file for more details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with any improvements or suggestions. I am but a humble assistant editor and programming is more a hobby than a profession, so I'm always open to feedback.

## Some Notes

This library is still in the 'finishing touches' phase, and as always, there may be undiscovered bugs. 

Due to differences in formatting between DOCX and TXT files, if you decide to convert to TXT manually, care needs to be taken to ensure line breaks are added in order for Avid not to read entire paragraphs as single lines. This is an issue which occurs regardless of whether you're using Avid Media Composer or `pyavc`. If in doubt, supply the Word file directly and allow the library to do this for you. However, the Word conversion feature still needs a bunch of testing (as at 08/25/2024). 

## Acknowledgments

`pyavc` would not be possible without the [pyavb library by mjiggidy](https://github.com/mjiggidy/pyavb), itself a fork of the [pyavb library by markreidvfx](https://github.com/markreidvfx/pyavb), which provided so many useful hints - as it turns out, AVC files are constructed much like AVB files. Who would have thought?
