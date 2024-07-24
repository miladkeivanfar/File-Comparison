## File Comparison Tool

This tool compares two CSV or Excel files based on a specified column and identifies rows that exist in one file but not the other. It writes the comparison results to a new Excel file.

## Features
- Compare two CSV or Excel files based on a specified column.
- Identify rows that exist in one file but not the other.
- Write the comparison results to a new Excel file.

## Usage

1- `git clone https://github.com/miladkeivanfar/File-Comparison.git`

2- `cd File-Comparison`

3- `pip3 install -r requirements.txt`

### Compare Excel

`python3 compare_files.py -t excel -f1 file1.xlsx -f2 file2.xlsx -c url -s1 Sheet1 -s2 Sheet1 -o output --silent`

### Compare CSV

`python3 compare_files.py -t csv -f1 file1.xlsx -f2 file2.xlsx -c url -o output`

### Options
```bash
-t, --type: Specify the type of files to compare (csv or excel).
-f1, --file1: Specify the name of the first file.
-f2, --file2: Specify the name of the second file.
-s1, --sheet1: Specify the name of the first sheet (for Excel files).
-s2, --sheet2: Specify the name of the second sheet (for Excel files).
-c, --column: Specify the column to compare.
-o, --output: Specify the name of the output file.
-s, --silent: Suppress logging and progress reporting.
```

### License
This tool is licensed under the MIT License.

