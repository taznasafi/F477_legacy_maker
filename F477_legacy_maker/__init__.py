import os

# create initial Data folder for input and output
if not os.path.exists(r'./data'):
    os.mkdir(r'./data')

input_path = r'./data/input'
output_path = r'./data/output'
zipfolder_path = r'./data/input/extracted_zipfiles'
output_csv_path = r"./data/output/csv"

if not os.path.exists(input_path):
    os.mkdir(input_path)
if not os.path.exists(output_path):
    os.mkdir(output_path)

if not os.path.exists(zipfolder_path):
    os.mkdir(zipfolder_path)

if not os.path.exists(output_csv_path):
    os.mkdir(output_csv_path)


