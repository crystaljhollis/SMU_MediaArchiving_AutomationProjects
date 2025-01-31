import os
import sys
import subprocess
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import pandas as pd
from moviepy.editor import VideoFileClip

# Function to install a package if it is not found
def install_package(package_name):
    try:
        __import__(package_name)
    except ImportError:
        print(f"{package_name} is not installed. Installing now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"{package_name} has been successfully installed!")

# Check and install pandas, moviepy, and openpyxl if not present
install_package("pandas")
install_package("moviepy")
install_package("openpyxl")

# Import the libraries after ensuring they are installed
import pandas as pd
from moviepy.editor import VideoFileClip

def get_resolution_label(file_path):
    try:
        clip = VideoFileClip(file_path)
        width, height = clip.size
        clip.reader.close()  # Close reader to release file
        if width >= 3840 and height >= 2160:  # 4K or higher
            return "_4K"
        elif width >= 3840 and height < 2160:  # Ultra HD
            return "_UHD"
        elif width == 1280 and height == 720:  # 720p resolution
            return "_720"
        elif width >= 1920 and height >= 1080:  # Full HD 1080p (Default)
            return ""  # Return an empty string for default 1080p to omit it from the filename
        else:
            return f"_{width}x{height}"  # Custom resolution label
    except Exception as e:
        print(f"Could not determine resolution for {file_path}. Error: {e}")
        return "_UnknownResolution"

def format_duration(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}h{minutes:02d}m{secs:02d}s"

def batch_rename_videos(directory, output_directory, catalog_number, appended_info=None, starting_number=1):
    video_extensions = {".mov", ".mp4", ".avi", ".mkv", ".mxf"}
    files = [f for f in os.listdir(directory) if os.path.splitext(f)[1].lower() in video_extensions]
    files.sort()  # Optional sorting for consistent renaming order

    video_details = []
    for idx, filename in enumerate(files, start=starting_number):
        file_extension = os.path.splitext(filename)[1]
        file_path = os.path.join(directory, filename)
        resolution_label = get_resolution_label(file_path)
        appended_info_str = f"_{appended_info}" if appended_info else ""
        new_filename = f"{catalog_number}V_{idx:03d}{resolution_label}{appended_info_str}{file_extension}"

        try:
            clip = VideoFileClip(file_path)
            clip_length = format_duration(clip.duration)  # Format duration in HHhMMmSSs
            clip.reader.close()
        except Exception as e:
            print(f"Could not determine length for {filename}. Error: {e}")
            clip_length = "Unknown"

        video_details.append({
            "Original File Name": filename,
            "Clip Name": new_filename,
            "Clip Length": clip_length  # Store formatted duration
        })

        old_file_path = os.path.join(directory, filename)
        new_file_path = os.path.join(output_directory, new_filename)
        os.rename(old_file_path, new_file_path)
        print(f"Renamed: {filename} --> {new_filename}")

    video_details_df = pd.DataFrame(video_details)
    output_excel_path = os.path.join(output_directory, "ShotList.xlsx")
    video_details_df.to_excel(output_excel_path, index=False)
    print(f"Spreadsheet saved as: {output_excel_path}")

def select_directory(title="Select Directory"):
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory(title=title)
    return directory

def main():
    # Show an initial message to guide the user
    messagebox.showinfo("Welcome!", "This script will batch rename video files and generate a shotlist in a spreadsheet.")

    # Prompt user to select the input directory
    messagebox.showinfo("Select Input Directory", "Please select the directory that contains the original video files to rename.")
    input_directory = select_directory("Select the directory containing the original video files to rename.")
    if not input_directory:
        messagebox.showwarning("No Input Directory", "No input directory selected. Exiting...")
        print("No input directory selected. Exiting...")
        return

    # Prompt user to select the output directory
    messagebox.showinfo("Select Output Directory", "Please select the directory where the renamed video files will be saved.")
    output_directory = select_directory("Select the directory where the renamed video files will be saved.")
    if not output_directory:
        messagebox.showwarning("No Output Directory", "No output directory selected. Exiting...")
        print("No output directory selected. Exiting...")
        return

    # Prompt user to enter the catalog number with a clear message
    messagebox.showinfo("Catalog Number", "Enter the catalog number that will be used as the base identifier in the filenames (e.g., 12345).")
    catalog_number = simpledialog.askstring("Catalog Number Input", "Enter the catalog number for these videos (e.g., 12345):\nThis number will be used as the base identifier in the filenames.")
    if not catalog_number:
        messagebox.showwarning("No Catalog Number", "No catalog number provided. Exiting...")
        print("No catalog number provided. Exiting...")
        return

    # Prompt user to enter custom appended info (optional)
    messagebox.showinfo("Appended Info", "You can add additional info to the filenames (e.g., video title, Interview, etc.). Leave it empty if not needed.")
    appended_info = simpledialog.askstring("Appended Info Input", "Enter any additional appended info (optional):\nLeave empty if not applicable.")

    # Prompt user to enter starting sequential number
    messagebox.showinfo("Starting Number", "Enter the starting number for the sequential numbering (e.g., 1, 2, 3...).")
    starting_number = simpledialog.askinteger("Starting Number Input", "Enter the starting sequential number (e.g., 1, 2, 3...):", initialvalue=1, minvalue=1)
    if not starting_number:
        messagebox.showwarning("No Starting Number", "No starting number provided. Using default value of 1.")
        starting_number = 1

    # Call the batch rename function with user inputs, including the starting number
    batch_rename_videos(input_directory, output_directory, catalog_number, appended_info, starting_number)

if __name__ == "__main__":
    # Initialize the tkinter root window and hide it before starting
    root = tk.Tk()
    root.withdraw()
    main()
