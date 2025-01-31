import os
import pandas as pd
from datetime import datetime
from tqdm import tqdm

# Function to automatically increment the output file name
def get_output_filename(base_name, extension):
    version = 1
    while os.path.exists(f"{base_name}_v{version}.{extension}"):
        version += 1
    return f"{base_name}_v{version}.{extension}"

# Prompt the user to load the combined CSV file produced by script 2
csv1_path = input("Enter the file path for the CSV file results from directory scan: ")
csv2_path = input("Enter the file path for the Photography Jobs CSV from FileMaker: ")

# Load the CSV files into DataFrames with a fallback encoding
try:
    df_csv1 = pd.read_csv(csv1_path, encoding='utf-8')
except UnicodeDecodeError:
    df_csv1 = pd.read_csv(csv1_path, encoding='ISO-8859-1')

try:
    df_csv2 = pd.read_csv(csv2_path, encoding='utf-8')
except UnicodeDecodeError:
    df_csv2 = pd.read_csv(csv2_path, encoding='ISO-8859-1')

# Define new columns order for final output
columns_order = [
    'Fiscal Year', 'Job Number', 'Neg Number', 'Video V or Photo D',
    'Folder Name', 'Date', 'File Path', 'Phase', 'Creator',
    'Folder Size (Bytes)', 'Folder Size (Readable)', 'File Count', 'Source File'
]

# Initialize an empty DataFrame to store the final result
final_df = pd.DataFrame(columns=columns_order)

# Function to nest folders under the appropriate job number or classify as "Mismatched"
def nest_folders():
    for _, job_row in tqdm(df_csv2.iterrows(), total=len(df_csv2), desc="Processing jobs"):
        job_number = job_row['Job Number']
        neg_number = str(job_row['Neg Number'])  # Convert to string for matching
        folder_name = job_row['Folder Name']
        fiscal_year = job_row['Fiscal Year']

        # Exact match for neg_number or job_number in File Path
        matching_folders = df_csv1[
            df_csv1['File Path'].apply(lambda x: f"/{neg_number}/" in x or f"/{job_number}/" in x)]

        if matching_folders.empty:
            # If no match is found, classify as "Mismatched"
            job_row['Job Number'] = "Mismatched"
            final_df.loc[len(final_df)] = job_row
        else:
            # Process matching folders
            for _, folder_row in matching_folders.iterrows():
                new_row = {
                    'Fiscal Year': fiscal_year,
                    'Job Number': job_number,
                    'Neg Number': neg_number,
                    'Video V or Photo D': job_row['Video V or Photo D'],
                    'Folder Name': folder_name,
                    'Date': job_row['Date'],
                    'File Path': folder_row['File Path'],
                    'Phase': job_row['Phase'],
                    'Creator': job_row['Creator'],
                    'Folder Size (Bytes)': folder_row['Folder Size (Bytes)'],
                    'Folder Size (Readable)': folder_row['Folder Size (Readable)'],
                    'File Count': folder_row['File Count'],
                    'Source File': folder_row['Source File']
                }
                final_df.loc[len(final_df)] = new_row

# Run the nesting function
nest_folders()

# Reorder the columns according to the specified order
final_df = final_df[columns_order]

# Prompt the user for a custom name for the new CSV output file
output_filename_base = input("Enter a custom name for the output CSV file: ")
output_filename = get_output_filename(f"{output_filename_base}_{datetime.today().strftime('%Y-%m-%d')}", "csv")

# Save the final DataFrame to the CSV file
final_df.to_csv(output_filename, index=False)

# Notify the user of the completion
print(f"CSV integration complete. The file has been saved as {output_filename}.")