#!/usr/bin/python3
import argparse
import pandas as pd
import logging
from tqdm import tqdm

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def compare_csv(file1, file2, column, output, silent=False):
    try:
        # Get the names of the CSV files
        file1_name = file1
        file2_name = file2

        # Get the column to compare from user
        column_to_compare = column

        # Load the CSV files
        file1 = pd.read_csv(file1_name)
        file2 = pd.read_csv(file2_name)

        # Check if the specified column exists in both files
        if column_to_compare not in file1.columns:
            raise ValueError(f"Column '{column_to_compare}' not found in file1.")
        if column_to_compare not in file2.columns:
            raise ValueError(f"Column '{column_to_compare}' not found in file2.")

        # Get the original column headers
        file1_headers = file1.columns.tolist()
        file2_headers = file2.columns.tolist()

        # Sort the files by the column to compare
        file1 = file1.sort_values(by=column_to_compare)
        file2 = file2.sort_values(by=column_to_compare)

        # Get the rows that exist in file1 but not in file2
        rows_to_delete = file1[~file1[column_to_compare].isin(file2[column_to_compare])]

        # Get the rows that exist in file2 but not in file1
        rows_to_add = file2[~file2[column_to_compare].isin(file1[column_to_compare])]

        # Create a new DataFrame for the comparison results
        comparison_results = pd.DataFrame({
            col: rows_to_delete[col].tolist() + rows_to_add[col].tolist()
            for col in set(file1_headers + file2_headers)
        })
        comparison_results['changes'] = ['Deleted'] * len(rows_to_delete) + ['Added'] * len(rows_to_add)

        # Write the comparison results to a new Excel file with original headers
        if not silent:
            logger.info(f'Writing comparison results to {output}.xlsx')
            for i in tqdm(range(len(comparison_results)), desc='Writing to Excel'):
                pass
        comparison_results.to_excel(f'{output}.xlsx', index=False)

    except FileNotFoundError:
        logger.error("One or both CSV files not found. Please check the file paths.")
    except ValueError as e:
        logger.error(str(e))
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")


def compare_excel(file1, file2, sheet1, sheet2, column, output, silent=False):
    try:
        # Get the names of the Excel files and sheets
        file1_name = file1
        file2_name = file2
        sheet1_name = sheet1
        sheet2_name = sheet2

        # Get the column to compare from user
        column_to_compare = column

        # Load the Excel files and sheets
        file1 = pd.read_excel(file1_name, sheet_name=sheet1_name)
        file2 = pd.read_excel(file2_name, sheet_name=sheet2_name)

        # Check if the specified column exists in both files
        if column_to_compare not in file1.columns:
            raise ValueError(f"Column '{column_to_compare}' not found in sheet '{sheet1_name}' of file1.")
        if column_to_compare not in file2.columns:
            raise ValueError(f"Column '{column_to_compare}' not found in sheet '{sheet2_name}' of file2.")

        # Get the original column headers
        file1_headers = file1.columns.tolist()
        file2_headers = file2.columns.tolist()

        # Sort the files by the column to compare
        file1 = file1.sort_values(by=column_to_compare)
        file2 = file2.sort_values(by=column_to_compare)

        # Get the rows that exist in file1 but not in file2
        rows_to_delete = file1[~file1[column_to_compare].isin(file2[column_to_compare])]

        # Get the rows that exist in file2 but not in file1
        rows_to_add = file2[~file2[column_to_compare].isin(file1[column_to_compare])]

        # Create a new DataFrame for the comparison results
        comparison_results = pd.DataFrame({
            col: rows_to_delete[col].tolist() + rows_to_add[col].tolist()
            for col in set(file1_headers + file2_headers)
        })
        comparison_results['changes'] = ['Deleted'] * len(rows_to_delete) + ['Added'] * len(rows_to_add)

        # Write the comparison results to a new Excel file with original headers
        if not silent:
            logger.info(f'Writing comparison results to {output}.xlsx')
            for i in tqdm(range(len(comparison_results)), desc='Writing to Excel'):
                pass
        comparison_results.to_excel(f'{output}.xlsx', index=False)

    except FileNotFoundError:
        logger.error("One or both Excel files not found. Please check the file paths.")
    except ValueError as e:
        logger.error(str(e))
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Compare two CSV or Excel files.")
    parser.add_argument('-t', '--type', type=str, required=True, choices=['csv', 'excel'],
                        help='Type of files to compare (csv or excel)')
    parser.add_argument('-f1', '--file1', type=str, required=True, help='file1 or old file')
    parser.add_argument('-f2', '--file2', type=str, required=True, help='file2 or new file')
    parser.add_argument('-s1', '--sheet1', type=str, default=None, help='sheet1 name in file1 '
                                                                        '(Case-sensitivity) (for Excel files only)')
    parser.add_argument('-s2', '--sheet2', type=str, default=None, help='sheet2 name in file2 '
                                                                        '(Case-sensitivity) (for Excel files only)')
    parser.add_argument('-c', '--column', type=str, required=True, help='one column for compare')
    parser.add_argument('-o', '--output', type=str, required=True, help='output name file for save changes')
    parser.add_argument('-s', '--silent', action='store_true', help='Suppress logging and progress reporting')
    args = parser.parse_args()

    if args.type == 'csv':
        if args.file1 and args.file2 and args.column and args.output:
            compare_csv(args.file1, args.file2, args.column, args.output, silent=args.silent)
        else:
            logger.error("For comparison CSV Files, You must enter file1, file2, column and output name file.")
    elif args.type == 'excel':
        if args.file1 and args.file2 and args.sheet1 and args.sheet2 and args.column and args.output:
            compare_excel(args.file1, args.file2, args.sheet1, args.sheet2, args.column, args.output,
                          silent=args.silent)
        else:
            logger.error(
                "For comparison Excel Files, You must enter file1, file2, sheet1, sheet2, column and output name file.")
    else:
        logger.error("Invalid file type. Please choose either 'csv' or 'excel'.")
