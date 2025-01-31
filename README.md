# **SMU Media Archiving Automation Projects**  

**Repository:** `SMU_MediaArchiving_AutomationProjects`  
**Author:** Crystal Hollis  
**Affiliation:** Contractor at Southern Methodist University (SMU)  
**Technologies Used:** Python, Shell Scripting, Pandas  

## **Overview**  
This repository contains automation scripts developed to improve media archiving workflows at Southern Methodist University (SMU). These scripts streamline processes such as batch file renaming and storage analysis, enhancing efficiency in digital asset management (DAM).  

Some files, such as proprietary datasets and spreadsheets used in the storage analysis, are omitted due to confidentiality. However, the repository includes scripts and general documentation outlining the methodology.  

## **Projects in This Repository**  

### **1. Batch Rename Script**  
- **Description:** Automates batch renaming of media files based on shot lists and metadata.  
- **Key Features:**  
  - Standardizes filenames for consistency in the DAM system  
  - Uses regex-based pattern matching to automate renaming  
  - Improves searchability and file organization  

### **2. Storage Analysis Scripts**  
- **Description:** Analyzes file storage directories to identify trends in file usage and space consumption.  
- **Key Features:**  
  - Uses **Pandas** for file size and metadata analysis  
  - Generates reports identifying redundant or oversized files  
  - Assists in optimizing storage management  
- **Note:** The Excel spreadsheet containing proprietary data has been omitted. The scripts included provide the methodology and can be adapted for other datasets.  

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
Each project has its own directory with a `README.md` providing specific usage instructions. Example usage for the **Batch Rename Script**:  

```bash
python batch_rename.py --source-folder /path/to/files --pattern "IMG_####"
```

## **Purpose and Impact**  
These automation projects were designed to improve the efficiency of media archiving processes by reducing manual effort and minimizing human error. The batch renaming script streamlines file organization, while the storage analysis tools provide insights into space usage, helping to optimize data storage strategies.  

## **Future Enhancements**  
- Additional automation for metadata extraction and categorization  
- Expanded storage analysis to include predictive file management recommendations  

## **Contributions & Contact**  
**Crystal Hollis** – `crystaljhollis@gmail.com`  
[GitHub Profile](https://github.com/crystaljhollis)  

For inquiries, suggestions, or collaboration, feel free to open an issue or submit a pull request.  

## **License**  
MIT License – Free to use, modify, and distribute with attribution.  

