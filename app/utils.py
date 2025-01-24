import pandas as pd

import csv

def parse_file(filepath):
    records = []
    try:
        with open(filepath, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                records.append({
                    "Date": row['Date'],
                    "Category": row['Category'],
                    "Amount": float(row['Amount']),
                    "Type": row['Type']
                })
        return records
    except Exception as e:
        return str(e)


def parse_file(file_path):
    try:
        df = pd.read_csv(file_path)
        return df.to_dict(orient='records')
    except Exception as e:
        return str(e)
