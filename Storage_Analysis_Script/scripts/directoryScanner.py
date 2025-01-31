import os
import math
import pandas as pd
from datetime import datetime
from tqdm import tqdm

# Function to calculate the size and file count of a local folder
def calculate_folder_size_and_file_count(folder_path):
    total_size = 0
    total_files = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                total_size += os.path.getsize(fp)
                total_files += 1
            except FileNotFoundError:
                print(f"File not found: {fp}, skipping.")
            except Exception as e:
                print(f"Error accessing file: {fp}, error: {e}")
    return total_size, total_files

# Human-Readable File Size Function
def human_readable_size(size_in_bytes):
    if size_in_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_in_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_in_bytes / p, 2)
    return f"{s} {size_name[i]}"

# Function to automatically increment the output file name
def get_output_filename(base_name, extension):
    version = 1
    while os.path.exists(f"{base_name}_v{version}.{extension}"):
        version += 1
    return f"{base_name}_v{version}.{extension}"

# Prompt for file paths
directory_path = input("Enter the file path location for the directory (server/local/external): ")
custom_name = input("What do you call this directory? ")

# Display initialization message
print("Initializing...do not close.")

# Calculate total directories for progress bar
total_dirs = sum([len(dirnames) for _, dirnames, _ in os.walk(directory_path)])

# Initialize lists to store directory details
folder_paths = []
folder_sizes = []
folder_sizes_readable = []
file_counts = []

# Iterate through directories with a progress bar
with tqdm(total=total_dirs, desc="Scanning directories") as pbar:
    for dirpath, dirnames, filenames in os.walk(directory_path):
        folder_size, file_count = calculate_folder_size_and_file_count(dirpath)
        folder_paths.append(dirpath)
        folder_sizes.append(folder_size)
        folder_sizes_readable.append(human_readable_size(folder_size))
        file_counts.append(file_count)
        pbar.update(1)  # Update the progress bar for each directory processed

# Prepare the DataFrame with the collected data
df = pd.DataFrame({
    'File Path': folder_paths,
    'Folder Size (Bytes)': folder_sizes,
    'Folder Size (Readable)': folder_sizes_readable,
    'File Count': file_counts
})

# Save the output CSV file
today = datetime.today().strftime('%Y-%m-%d')
output_csv_path = get_output_filename(f"{custom_name}_{today}", "csv")
df.to_csv(output_csv_path, index=False)
print(f"Directory scan completed. Results saved to: {output_csv_path}")