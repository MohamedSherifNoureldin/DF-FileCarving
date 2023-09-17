import argparse
import csv
import re
from colorama import Fore, Style
import os


# function to parse csv magic headers file to dictionary
def get_headers(file_path):
    headers_count = 0
    headers = {}
    # parse csv file to dictionary
    try:
        with open(file_path, 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                key = key = row[0].strip().lower()
                value = row[1].strip().lower()
                if key in headers:
                    headers[key].append(value)
                else:
                    headers[key] = [value]
                headers_count += 1
        print(Fore.GREEN + "[+] SUCCESS : " + Style.RESET_ALL + f"Configuration file {file_path} read.")
        print(Fore.GREEN + "[+] SUCCESS : " + Style.RESET_ALL + f"Loaded {len(headers)} file types and {headers_count} headers.")
        print()
        return headers
    except Exception as e:
        print(Fore.RED + "[-] ERROR : " + Style.RESET_ALL + f"Error reading configuration file {file_path}.")
        print(Fore.RED + "[-] ERROR : " + Style.RESET_ALL + f"{e}")
        exit()

# function to read file as hex
def get_file_hex(file_path):
    # read file as hex
    try:
        with open(file_path, 'rb') as file:
            hex_data = file.read().hex()
        return hex_data
    except Exception as e:
        print(Fore.RED + "[-] ERROR : " + Style.RESET_ALL + f"Error reading file {file_path}.")
        print(Fore.RED + "[-] ERROR : " + Style.RESET_ALL + f"{e}")
        exit()

# function to get file type from magic headers
def get_file_type(hex_data, headers):
    # get file type
    for key in headers:
        for header in headers[key]:
            if hex_data.startswith(header):
                return key
    return 'unknown'

# function to search hex file for hidden files using magic headers and return dictionary of found files and indexes
def get_files_and_indexes(hex_data, headers):
    print("Searching file for headers...")

    found_files = {}
    # search file for headers
    for key in headers:
        for header in headers[key]:
            matches = re.finditer(header, hex_data)
            for match in matches:
                start_index = match.start()
                found_files[start_index] = key
                start_index_hex = hex(start_index)
                print(Fore.GREEN + "[+] FOUND : " + Style.RESET_ALL + f"{key.upper()} Header found at index {start_index_hex}.")

    
    found_files = dict(sorted(found_files.items()))
    found_indexes = sorted(list(found_files.keys()))
    print()
    print(Fore.GREEN + "[+] SUCCESS : " + Style.RESET_ALL + f"Found {len(found_files)} files.")
    print()
    return (found_files, found_indexes)

# function to extract files from hex data using found files and indexes to output directory
def extract_files(hex_data, found_files, found_indexes, output_dir):
    print("Extracting & spliting files...")
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # create dictionary to hold number of files found for each type
    file_counts = {}
    for file_type in found_files.values():
        file_counts[file_type] = 0

    # Split files
    for i in range(len(found_indexes)):
        if i == len(found_indexes) - 1:
            file_data = hex_data[found_indexes[i]:]
        else:
            file_data = hex_data[found_indexes[i]:found_indexes[i + 1]]
        file_type = found_files[found_indexes[i]]
        file_count = file_counts[file_type]
        file_name = os.path.join(output_dir, f"{file_type}_{file_count}.{file_type}")
        file_counts[file_type] += 1
        with open(file_name, 'wb') as file:
            file.write(bytes.fromhex(file_data))
        print(Fore.GREEN + "[+] SUCCESS : " + Style.RESET_ALL + f"File {file_name} written.")

# function to combine files into a single file
def combine_files(input_files, output_file):
    print("Combining files...")
    print(Fore.GREEN + "[+] " + Style.RESET_ALL + f"Provided {len(input_files)} files to be combined.")
    print()

    # Create the directory path for the output file if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir and os.path.exists(output_dir):
        os.makedirs(output_dir)

    # combine files
    try:
        with open(output_file, 'wb') as output:
            for input_file in input_files:
                with open(input_file, 'rb') as input:
                    output.write(input.read())
                print(Fore.GREEN + "[+] SUCCESS : " + Style.RESET_ALL + f"File {input_file} written to {output_file}.")
    except Exception as e:
        print(Fore.RED + "[-] ERROR : " + Style.RESET_ALL + f"Error combining files.")
        print(Fore.RED + "[-] ERROR : " + Style.RESET_ALL + f"{e}")
        exit()


def main():
    parser = argparse.ArgumentParser(description='Forensics tool to extract multiple files from a single file using magic headers or combine multiple files into a single file.')
    subparsers = parser.add_subparsers(dest='mode', help='Choose mode: crave or combine', required=True)

    crave_parser = subparsers.add_parser('crave', help='Extract multiple files from a single file using magic headers.')
    crave_parser.add_argument('magic_headers_file', help='CSV Configuration file containing magic headers to look for.')
    crave_parser.add_argument('input_file', help='File to extract files from.')
    crave_parser.add_argument('-o', '--output_dir',  help='Directory to write files to. Defaults to current directory.', default='.')

    combine_parser = subparsers.add_parser('combine', help='Combine multiple files into a single file.')
    combine_parser.add_argument('input_files', nargs='+', help='Files to combine into a single file.')
    combine_parser.add_argument('output_file', help='Output file to write to.')

    args = parser.parse_args()

    if(args.mode == 'crave'):
        headers = get_headers(args.magic_headers_file)
        hex_data = get_file_hex(args.input_file)
        (found_files, found_indexes) = get_files_and_indexes(hex_data, headers)
        extract_files(hex_data, found_files, found_indexes, args.output_dir)
    elif(args.mode == 'combine'):
        combine_files(args.input_files, args.output_file)
    else:
        print('Invalid mode.')

if __name__ == "__main__":
    main()