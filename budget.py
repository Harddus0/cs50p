import pandas as pd
import chardet
import csv

def detect_encoding_and_separator(csv_filename):
    """Detects file encoding and CSV separator"""
    
    # Detect encoding
    with open(csv_filename, 'rb') as f:
        result = chardet.detect(f.read())
        encoding = result['encoding']
    
    # Detect separator
    with open(csv_filename, 'r', encoding=encoding) as f:
        separator = csv.Sniffer().sniff(f.readline()).delimiter

    return encoding, separator


def load_budget_file():
    """Calculates cost based on csv budget file"""

    budget_filename = input("Enter budget file name or directory: ").strip()
    
    if budget_filename.endswith(".csv"):
        pass
    else:
        budget_filename = budget_filename + ".csv"
    
    encoding, separator = detect_encoding_and_separator(budget_filename)

    return pd.read_csv(budget_filename, sep=separator, encoding=encoding)