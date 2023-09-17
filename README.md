# Digital Forensics File Carving Tool
Mohamed Sherif Noureldin, 900203758
## Overview
This Python-based Forensics tool performs two primary operations:
1. Extracts multiple files embedded in a single file using magic headers, a mode known as `crave`.
2. Combines multiple files into a single file, a mode known as `combine`.

## Installation
To run this tool, Python is required. You also need the `argparse`, `csv`, `re`, and `colorama` modules. If these are not installed, use the following commands:

```
pip install argparse
pip install csv
pip install re
pip install colorama
```

## How to Use
This tool is executed from the command line with the following syntax:
```shell
python3 main.py [mode] [arguments]
```
Where:
- `[mode]` can be either `crave` or `combine`.
- `[arguments]` are the specific arguments for each mode.

The tool offers the following modes:

### 1. Crave Mode
Extracts multiple files from a single file using magic headers.

#### Usage
```shell
python3 main.py crave magic_headers_file input_file [-o output_dir]
```

#### Parameters
- `magic_headers_file`: A CSV configuration file containing magic headers to look for. The file should contain key-value pairs of file types and their corresponding magic headers.
- `input_file`: The file from which files should be extracted.
- `output_dir` (Optional): Directory to write the extracted files to. Defaults to the current directory if not specified.

#### Example
```shell
python3 main.py crave magic.csv test2 -o found_files
```
![Crave Mode Example Run](images/crave.png "crave mode example run")


### 2. Combine Mode
Combines multiple files into a single file.

#### Usage
```shell
python3 main.py combine input_files output_file
```

#### Parameters
- `input_files`: One or more files to combine into a single file.
- `output_file`: The output file to which the combined data should be written.

#### Example
```shell
python3 main.py combine test test2 combined_test
```
![Combine Mode Example Run](images/combine.png "combine mode example run")


## Functions

Here is a brief description of each function in the tool:

- `get_headers(file_path)`: Parses a CSV magic headers file into a dictionary.
- `get_file_hex(file_path)`: Reads a file as hexadecimal data.
- `get_file_type(hex_data, headers)`: Determines the file type from magic headers.
- `get_files_and_indexes(hex_data, headers)`: Searches hexadecimal file for hidden files using magic headers and returns a dictionary of found files and indexes.
- `extract_files(hex_data, found_files, found_indexes, output_dir)`: Extracts files from hexadecimal data using found files and indexes, writing them to an output directory.
- `combine_files(input_files, output_file)`: Combines provided input files into a single output file.

## Error Handling
The tool includes extensive error handling, with specific error messages in case of failed operations such as file reading or writing, and CSV parsing. The output messages are color-coded for better visibility.

## Implementation Details

Below are more detailed explanations of how each function works.

### get_headers(file_path)
This function is used to parse a CSV file that contains magic headers. It reads the file line by line, creating a dictionary where the key is the file type and the value is a list of magic headers for that type. If an error occurs during the file reading process, the function prints an error message and terminates the program. This function is used in the 'crave' mode to define the magic headers that the program will search for in the input file.

### get_file_hex(file_path)
This function reads a file and returns its hexadecimal representation. It opens the file in binary mode and reads all of its contents. If an error occurs during this process, the function prints an error message and terminates the program.

### get_file_type(hex_data, headers)
This function accepts two parameters: a string containing hexadecimal data and a dictionary containing magic headers. It iterates through the dictionary and checks if the hexadecimal data starts with any of the magic headers. If a match is found, the corresponding file type is returned. If no match is found, the function returns 'unknown'.

### get_files_and_indexes(hex_data, headers)
This function searches for magic headers within the hexadecimal data. It iterates through each magic header for each file type and uses a regular expression to find all matches within the hexadecimal data. Each match's start index and corresponding file type are stored in a dictionary. The dictionary and a sorted list of all found indexes are returned.

### extract_files(hex_data, found_files, found_indexes, output_dir)
This function is used to extract files from the hexadecimal data. For each file found in the 'get_files_and_indexes' function, the function calculates the start and end indexes of the file in the hexadecimal data, converts the relevant hexadecimal data back to binary, and writes it to a file. The file is named using the file type and a count of files of that type that have been written so far, and it's written to the output directory specified by the user.

### combine_files(input_files, output_file)
This function combines multiple files into a single file. It reads each file in the 'input_files' list in binary mode, and writes its contents to the 'output_file'. The output file is created in binary mode, allowing it to accept and correctly write the binary data from the input files. 

### main()
This is the main function of the script, which handles argument parsing and calls the appropriate functions based on the selected mode. It uses the argparse module to parse command line arguments. There are two modes available, 'crave' and 'combine'. In 'crave' mode, the function calls the 'get_headers', 'get_file_hex', 'get_files_and_indexes', and 'extract_files' functions to extract files from the input file. In 'combine' mode, the function calls the 'combine_files' function to combine the input files into a single file.

## Restrictions and Limitations
The tool extracts files by searching for their magic headers. The tool determines the end of the file by finding the start of another file and doesn't have the functionality to look for file footers indicating the end of the file. This means that for example if we have a PDF file including 5 images, the tool will extract all the images correctly but will result in a corrupted PDF file because when searching for magic headers the tool will first find the header of the pdf file followed by the header of the first image. This will indicate to the tool that the pdf file ends at the start of the first image, resulting in a corrupted pdf file. The tool was implemented this way due to following the provided instruction and assumption that the tool should extract files from one header to the other.
