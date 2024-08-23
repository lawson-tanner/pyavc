# pyavc

\`pyavc\` is a Python library that allows you to convert DOCX or TXT files into a specific output format. It can be used both as a command-line tool and as a library within your Python scripts.

## Installation

To install \`pyavc\`, you can use \`pip3\`:

\`\`\`bash
pip3 install pyavc
\`\`\`

## Usage

### As a Python Library

The main function exposed to end users is \`convert\`. This function allows you to convert a DOCX or TXT file and save the result in a specified output directory.

#### Function Signature

\`\`\`python
convert(filepath: os.Path, output_dir: os.Path, output_name=None)
\`\`\`

#### Parameters

- **\`filepath\`** (\`os.Path\`): The path to the input DOCX or TXT file.
- **\`output_dir\`** (\`os.Path\`): The path to the output directory where the converted file will be saved.
- **\`output_name\`** (\`str\`, optional): The name of the output file (without extension). If not provided, the output file will be named based on the input file name.

#### Example Usage

\`\`\`python
import avc

# Convert a TXT file and save the output
avc.convert('/path/to/input.txt', '/path/to/output/dir')

# Convert a DOCX file and specify a custom output name
avc.convert('/path/to/input.docx', '/path/to/output/dir', output_name='custom_name')
\`\`\`

### Command-Line Usage

\`pyavc\` can also be used from the command line to quickly convert files.

#### Syntax

\`\`\`bash
pyavc -i <path-to-input-file> -o <path-to-output-dir> [-n <output-name>]
\`\`\`

#### Parameters

- **\`-i, --input\`**: Path to the input DOCX or TXT file.
- **\`-o, --output_dir\`**: Path to the output directory where the converted file will be saved.
- **\`-n, --output_name\`**: (Optional) Name of the output file (without extension). If not provided, the output file will be named based on the input file name.

#### Example Commands

\`\`\`bash
# Convert a TXT file and save the output
pyavc -i /path/to/input.txt -o /path/to/output/dir

# Convert a DOCX file and specify a custom output name
pyavc -i /path/to/input.docx -o /path/to/output/dir -n custom_name
\`\`\`

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with any improvements or suggestions.

## Acknowledgments

Special thanks to all contributors and users of \`pyavc\`.
