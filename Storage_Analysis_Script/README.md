# **Storage Analysis Project**  

**Repository:** `StorageAnalysisProject`  
**Author:** Crystal Hollis  
**Affiliation:** Contractor at Southern Methodist University (SMU)  
**Technologies Used:** Python, Pandas, OS Module  

## **Overview**  
The **Storage Analysis Project** automates the scanning and analysis of file storage directories. It provides insights into storage usage, job number tracking, and CSV data integration for improved digital asset management. This project helps identify redundant files, track job numbers, and generate reports to optimize data storage strategies.

**Note:** Only the scripts are included in this repository. Input data files, including proprietary spreadsheets, have been omitted.

---

## **Project Structure**  

```
StorageAnalysisProject/
│── input_data/                 # Placeholder for input files (Not included in repo)
│── output/                      # Folder for storing generated reports and logs
│── scripts/                     # Contains Python scripts for storage analysis
│   ├── dataStorageAnalysis.py
│   ├── directoryScanner.py
│   ├── directoryScannerCSVIntegrator.py
│   ├── jobNumberCheck.py
│── README.md
```

---

## **Scripts Overview**  

### **1. dataStorageAnalysis.py**  
- Analyzes storage directories to assess space usage, identify large files, and generate summary reports.  
- Uses `pandas` for data processing and `os` for directory traversal.  

### **2. directoryScanner.py**  
- Scans directories and subdirectories for media files and other assets.  
- Provides a structured output of directory contents, including file sizes and extensions.  

### **3. directoryScannerCSVIntegrator.py**  
- Extends the `directoryScanner.py` functionality by integrating scan results with external CSV datasets.  
- Helps match scanned file data with existing storage records for better tracking.  

### **4. jobNumberCheck.py**  
- Checks for job numbers within filenames and cross-references them against expected values.  
- Useful for identifying missing or improperly labeled files.  

---

## **Installation & Usage**  

### **Prerequisites**  
- Python 3.x  
- Required libraries:  
  ```bash
  pip install pandas numpy os argparse
  ```

### **Clone the Repository**  
```bash
git clone https://github.com/crystaljhollis/StorageAnalysisProject.git
cd StorageAnalysisProject/scripts
```

### **Running the Scripts**  
Each script has its own specific use case. Below are example commands to execute them:

**Run Directory Scanner:**  
```bash
python directoryScanner.py --path /path/to/directory
```

**Run Storage Analysis:**  
```bash
python dataStorageAnalysis.py --input /path/to/input_data
```

**Run CSV Integrator:**  
```bash
python directoryScannerCSVIntegrator.py --csv /path/to/existing_data.csv
```

**Run Job Number Check:**  
```bash
python jobNumberCheck.py --job-list /path/to/job_numbers.csv
```

---

## **Project Purpose & Benefits**  
This project was developed to improve storage management at SMU by:  
✔ Automating storage analysis and reducing manual tracking efforts  
✔ Identifying large or redundant files for better storage utilization  
✔ Ensuring job number accuracy across file directories  

---

## **Possible Future Enhancements**  
- Add logging functionality for better debugging and tracking  
- Improve CSV integration with additional metadata processing  
- Develop visualization tools for storage trends  

---

## **Contributions & Contact**  
**Crystal Hollis** – `crystaljhollis@gmail.com`  
[GitHub Profile](https://github.com/crystaljhollis)  

For inquiries, feature requests, or collaboration, feel free to open an issue or submit a pull request.

---

## **License**  
MIT License – Free to use, modify, and distribute with attribution.  

