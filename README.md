# **SMU Media Archiving Automation Projects**  

**Repository:** `SMU_MediaArchiving_AutomationProjects`  
**Author:** Crystal Hollis  
**Affiliation:** Contractor at Southern Methodist University (SMU)  
**Technologies Used:** Python, Shell Scripting, Pandas  

## **Overview**  
This repository contains automation scripts developed to improve media archiving workflows at Southern Methodist University (SMU). These scripts streamline processes such as batch file renaming and storage analysis, enhancing efficiency in digital asset management (DAM).  

Some files, such as proprietary datasets and spreadsheets used in the storage analysis, are omitted due to confidentiality. However, the repository includes scripts and general documentation outlining the methodology.  

---

## **Projects in This Repository**  

### **1. Batch Rename Script**  
- **Description:** Automates batch renaming of video files based on structured naming conventions. Users provide a catalog number, sequential numbering, and optional descriptions, while the script automatically detects video resolution and appends it to filenames. A **shotlist spreadsheet** is generated to document the renamed files.  
- **Key Features:**  
  - Renames video files in bulk based on user input.  
  - Automatically detects and appends video resolution to filenames.  
  - **Does not duplicate files—renaming is applied in place** (backups recommended).  
  - Generates a **shotlist spreadsheet** listing renamed files.  
  - Checks for required dependencies and installs missing libraries automatically.  

---

### **2. Storage Analysis Scripts**  
- **Description:** The storage analysis scripts scan directories, compile file data, and generate structured reports for optimizing storage management. These tools help track file sizes, detect redundant files, and ensure consistency in naming conventions.  
- **Key Features:**  
  - **Directory scanning**: Extracts file paths, sizes, and extensions from directories and subdirectories.  
  - **Job number validation**: Cross-references filenames against expected **job numbers** to identify missing or misnamed files.  
  - **CSV integration**: Merges scan results with external datasets for deeper analysis.  
  - **Storage efficiency analysis**: Generates reports to identify large files and redundant data.  
  - Uses **Pandas** for data processing and report generation.  

---

## **Installation & Usage**  

### **Prerequisites**  
- Python 3.x  
- Required libraries: `pandas`, `numpy`, `os`, `shutil`, `argparse`, `regex`, `matplotlib`  

### **Clone This Repository**  
```bash
git clone https://github.com/crystaljhollis/SMU_MediaArchiving_AutomationProjects.git
cd SMU_MediaArchiving_AutomationProjects
```

### **Running the Scripts**  
Each project has its own directory with a `README.md` providing specific usage instructions.  

**Run Batch Rename Script:**  
```bash
python batchRename.py
```
The script will prompt the user for input, including the folder location, catalog number, sequential number, and optional descriptions.  

**Run Storage Analysis Script:**  
```bash
python dataStorageAnalysis.py --input /path/to/storage/directory
```
This script scans the directory and generates reports on storage usage.  

---

## **Project Purpose & Benefits**  
These automation projects were designed to improve the efficiency of media archiving processes by reducing manual effort and minimizing human error. The **batch renaming script** ensures consistent file naming, while the **storage analysis tools** provide insights into space usage and missing files, helping to optimize data storage strategies.  

---

## **Future Enhancements**  
- Additional automation for metadata extraction and categorization.  
- Expanded storage analysis with predictive file management recommendations.  

---

## **Contributions & Contact**  
**Crystal Hollis** – `crystaljhollis@gmail.com`  
[GitHub Profile](https://github.com/crystaljhollis)  

For inquiries, suggestions, or collaboration, feel free to open an issue or submit a pull request.  

---

## **License**  
MIT License – Free to use, modify, and distribute with attribution.  

