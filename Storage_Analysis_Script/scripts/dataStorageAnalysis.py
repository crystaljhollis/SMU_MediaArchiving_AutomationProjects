import pandas as pd
import re
from tkinter import Tk, filedialog
from tqdm import tqdm

# Function to open a file dialog and get the file path
def select_file(prompt):
    root = Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(title=prompt)
    return file_path

# Prompt user to select the CSV file
csv_path = select_file("Select the combined CSV file")

# Load the CSV file with tqdm progress bar
print("Loading CSV file...please wait.")
df = pd.read_csv(csv_path)

# Ensure that the relevant columns are in the correct format
df['Folder Size (Bytes)'] = pd.to_numeric(df['Folder Size (Bytes)'], errors='coerce')

# Remove duplicate Neg Numbers
df_no_duplicates = df.drop_duplicates(subset='Neg Number')

# 1. Total number of Job Numbers in Fiscal Years 2023 and 2024
jobs_2023_2024 = df_no_duplicates[(df_no_duplicates['Fiscal Year'] == 2023) | (df_no_duplicates['Fiscal Year'] == 2024)]
total_jobs_2023_2024 = jobs_2023_2024['Job Number'].nunique()
print(f"Total number of Job Numbers in Fiscal Years 2023 and 2024: {total_jobs_2023_2024}")

# 2. Total number of Job Numbers to date in Fiscal Year 2025
jobs_2025 = df_no_duplicates[df_no_duplicates['Fiscal Year'] == 2025]
total_jobs_2025 = jobs_2025['Job Number'].nunique()
print(f"Total number of Job Numbers to date in Fiscal Year 2025: {total_jobs_2025}")

# 3. Total number of Jobs/Neg numbers between FY 2015-2025
jobs_2015_2025 = df_no_duplicates[(df_no_duplicates['Fiscal Year'] >= 2015) & (df_no_duplicates['Fiscal Year'] <= 2025)]
total_jobs_2015_2025 = jobs_2015_2025['Job Number'].nunique()
total_negs_2015_2025 = jobs_2015_2025['Neg Number'].nunique()
print(f"Total number of Jobs between FY 2015-2025: {total_jobs_2015_2025}")
print(f"Total number of Neg Numbers between FY 2015-2025: {total_negs_2015_2025}")

# 4. Total number of Neg numbers with "Donor" and "Campaign" in the Folder Name in the file path/File Name field (Between FY 2015-2025)
donor_campaign_negs = df_no_duplicates[(df_no_duplicates['File Path'].str.contains('Donor|Campaign', flags=re.IGNORECASE, na=False)) & (df_no_duplicates['Fiscal Year'] >= 2015) & (df_no_duplicates['Fiscal Year'] <= 2025)]
total_donor_campaign_negs = donor_campaign_negs['Neg Number'].nunique()
print(f"Total number of Neg numbers associated with 'Donor' and 'Campaign' between FY 2015-2025: {total_donor_campaign_negs}")

# 5. Average size in GB of Donor and Campaign related Jobs (Between FY 2020-2025)
donor_campaign_jobs_2020_2025 = df_no_duplicates[(df_no_duplicates['File Path'].str.contains('Donor|Campaign', flags=re.IGNORECASE, na=False)) & (df_no_duplicates['Fiscal Year'] >= 2020) & (df_no_duplicates['Fiscal Year'] <= 2025)]
avg_donor_campaign_size = donor_campaign_jobs_2020_2025['Folder Size (Bytes)'].mean() / 1e9  # Convert to GB (decimal system)
print(f"Average size (Gigabytes) of Donor and Campaign related Jobs (Between FY 2020-2025): {avg_donor_campaign_size:.2f} GB")

# 6. Average size in GB of Jobs in FY 2023 and FY 2024
avg_jobs_2023_2024_size = jobs_2023_2024['Folder Size (Bytes)'].mean() / 1e9  # Convert to GB (decimal system)
print(f"Average size (Gigabytes) of Jobs in FY 2023 and FY 2024: {avg_jobs_2023_2024_size:.2f} GB")

# 7. Average size in GB of all Jobs Between FY 2015-2025
avg_jobs_2015_2025_size = jobs_2015_2025['Folder Size (Bytes)'].mean() / 1e9  # Convert to GB (decimal system)
print(f"Average size (Gigabytes) of all Jobs between FY 2015-2025: {avg_jobs_2015_2025_size:.2f} GB")

# 8. Average size in GB of Photos in FY 2023 and Between FY 2015-2025
photos_2023 = jobs_2023_2024[jobs_2023_2024['Video V or Photo D'] == 'Photo']
photos_2015_2025 = jobs_2015_2025[jobs_2015_2025['Video V or Photo D'] == 'Photo']

avg_photos_2023_size = photos_2023['Folder Size (Bytes)'].mean() / 1e9  # Convert to GB (decimal system)
avg_photos_2015_2025_size = photos_2015_2025['Folder Size (Bytes)'].mean() / 1e9  # Convert to GB (decimal system)

print(f"Average size (Gigabytes) of Photos in FY 2023: {avg_photos_2023_size:.2f} GB")
print(f"Average size (Gigabytes) of Photos between FY 2015-2025: {avg_photos_2015_2025_size:.2f} GB")

# 9. Average size in GB of Videos in FY 2023 and Between FY 2015-2025
videos_2023 = jobs_2023_2024[jobs_2023_2024['Video V or Photo D'] == 'Video']
videos_2015_2025 = jobs_2015_2025[(jobs_2015_2025['Video V or Photo D'] == 'Video')]

avg_videos_2023_size = videos_2023['Folder Size (Bytes)'].mean() / 1e9  # Convert to GB (decimal system)
avg_videos_2015_2025_size = videos_2015_2025['Folder Size (Bytes)'].mean() / 1e9  # Convert to GB (decimal system)

print(f"Average size (Gigabytes) of Videos in FY 2023: {avg_videos_2023_size:.2f} GB")
print(f"Average size (Gigabytes) of Videos between FY 2015-2025: {avg_videos_2015_2025_size:.2f} GB")

# 10. Total number of folders and folder size that don't have job numbers and is pending processing
pending_processing = df_no_duplicates[df_no_duplicates['Job Number'].isna()]
total_pending_processing_folders = pending_processing.shape[0]
total_pending_processing_size = pending_processing['Folder Size (Bytes)'].sum() / 1e9  # Convert to GB (decimal system)
print(f"Total number of folders pending processing: {total_pending_processing_folders}")
print(f"Total size of folders pending processing: {total_pending_processing_size:.2f} GB")

# 11. Total number of folders and folder size that are not in /Volumes/DEAphoto$
non_deaphoto_folders = df_no_duplicates[~df_no_duplicates['File Path'].str.contains('/Volumes/DEAphoto$', na=False)]
total_non_deaphoto_folders = non_deaphoto_folders.shape[0]
total_non_deaphoto_size = non_deaphoto_folders['Folder Size (Bytes)'].sum() / 1e9  # Convert to GB (decimal system)
print(f"Total number of folders not in /Volumes/DEAphoto$: {total_non_deaphoto_folders}")
print(f"Total size of folders not in /Volumes/DEAphoto$: {total_non_deaphoto_size:.2f} GB")