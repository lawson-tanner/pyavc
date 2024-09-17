# pyavc

`pyavc` is a Python library that allows you to convert DOCX or TXT files into Avid Script (.avc) files. It can be used both as a command-line tool and as a library within your Python scripts.

This project is not affiliated with Avid or Avid Media Composer, it is simply an open source helper library to make fellow AEs' lives a bit easier.

## Installation

To install `pyavc`, you can use `pip3`:

```bash
pip3 install pyavc
```

## Import Syntax

Use the following syntax to import the functionality into your Python script:

```python
from avc.core import convert
```

## Usage

### As a Python Library

The main (and only) method provided is `convert`. It allows you to convert a DOCX or TXT file and save the result to a specified output directory.

```python
convert(filepath, output_dir, output_name=None, text_width=80)
```

#### Parameters

- **`filepath`** (`os.Path`): The path to the input DOCX or TXT file. If using a TXT file, it must be encoded as UTF-8.
- **`output_dir`** (`os.Path`): The path to the output directory where the converted file will be saved.
- **`output_name`** (`str`, optional): The name of the output file (without extension). If not provided, the output file will be named based on the input file name. Whether this argument is provided or not, `pyavc` will never overwrite existing files, but will append consecutive numbers to the end of the file name.
- **`text_width`** (`int`, optional): The maximum length, in characters, before a line break is inserted. By default, it is set to 80 characters. This is done to avoid the classic issue of entire paragraphs being read as a single line.

#### Example Usage

```python
from avc.core import convert

# Convert a TXT file and save the output
convert('/path/to/input.txt', '/path/to/output/dir')

# Convert a DOCX file and specify a custom output name
convert('/path/to/input.docx', '/path/to/output/dir', output_name='custom_name')
```

### Command-Line Usage

`pyavc` can also be used from the command line to quickly convert files.

#### Syntax

```bash
pyavc -i <path-to-input-file> -o <path-to-output-dir> [-n <output-name>] [-t <text-width>]
```

#### Parameters

- **`-i, --input`**: Path to the input DOCX or TXT file.
- **`-o, --output_dir`**: Path to the output directory where the converted file will be saved.
- **`-n, --output_name`**: (Optional) Name of the output file (without extension). If not provided, the output file will be named based on the input file name.
- **`text_width`** (`int`, optional): The maximum length, in characters, before a line break is inserted. By default, it is set to 80 characters. 

#### Example Commands

```bash
# Convert a TXT file and save the output
pyavc -i /path/to/input.txt -o /path/to/output/dir

# Convert a DOCX file and specify a custom output name
pyavc -i /path/to/input.docx -o /path/to/output/dir -n custom_name

# Convert a DOCX file and specify a custom output name plus custom text width
pyavc -i /path/to/input.docx -o /path/to/output/dir -n custom_name -t text-width
```

## License

This project is licensed under the GPL 3.0 License. See the [LICENSE](LICENSE) file for more details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with any improvements or suggestions. I am but a humble assistant editor and programming is more a hobby than a profession, so I'm always open to feedback.

## Some Notes

This library is still in the 'finishing touches' phase, and as always, there may be undiscovered bugs. 

## Acknowledgments

`pyavc` would not be possible without the [pyavb library by markreidvfx](https://github.com/markreidvfx/pyavb), which provided so many useful hints. As it turns out, AVC files are constructed much like AVB files. Who would have thought?
