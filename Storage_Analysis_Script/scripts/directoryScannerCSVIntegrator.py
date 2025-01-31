import os
import pandas as pd
from datetime import datetime
from tkinter import Tk, filedialog

# Function to automatically increment the output file name
def get_output_filename(base_name, extension):
    version = 1
    while os.path.exists(f"{base_name}_v{version}.{extension}"):
        version += 1
    return f"{base_name}_v{version}.{extension}"

# Function to check if required columns are present
def check_required_columns(df):
    required_columns = ['File Path', 'Folder Size (Bytes)', 'Folder Size (Readable)', 'File Count']
    return all(col in df.columns for col in required_columns)

# Initialize Tkinter root for file dialog
Tk().withdraw()

# Prompt user to specify multiple CSV files to combine
print("Please select the CSV files to combine.")
csv_files = filedialog.askopenfilenames(title="Select CSV Files", filetypes=[("CSV files", "*.csv")])

# Print initialization message
print("Initializing...please wait.")

# List to hold DataFrames
dfs = []

# Process each CSV file
for file in csv_files:
    try:
        df = pd.read_csv(file)
        if check_required_columns(df):
            df['Source File'] = os.path.basename(file)  # Add column with the name of the original CSV
            dfs.append(df)
        else:
            print(f"CSV skipped (missing required columns): {file}")
    except Exception as e:
        print(f"Error reading {file}: {e}")

# Check if any valid CSVs were processed
if not dfs:
    print("No valid CSVs to combine. Exiting.")
else:
    # Print combining message
    print("Combining CSVs...")

    # Combine all DataFrames
    combined_df = pd.concat(dfs, ignore_index=True)

    # Print exporting message
    print("CSV integration complete. Exporting...")

    # Prompt user for a custom name
    custom_name = input("Enter the custom name for the combined CSV file: ")

    # Save the combined CSV file
    today = datetime.today().strftime('%Y-%m-%d')
    output_csv_path = get_output_filename(f"{custom_name}_{today}", "csv")
    combined_df.to_csv(output_csv_path, index=False)

    # Print completion message
    print(f"Exporting complete. Combined CSV saved to: {output_csv_path}")