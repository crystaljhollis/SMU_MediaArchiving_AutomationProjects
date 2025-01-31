# **Batch Rename Script – Storage Management Automation**  

**Author:** Crystal Hollis  
**Affiliation:** Contractor at Southern Methodist University (SMU)  
**Technologies Used:** Python, Pandas, MoviePy, OpenPyXL  

## **Overview**  
This repository contains a **batch renaming script** designed to streamline media file organization and storage management. It automates the process of renaming files according to predefined patterns, ensuring consistency in digital asset management.  

The script also includes **storage analysis features** to assist in optimizing file organization, improving accessibility, and reducing redundancy.  

---

## **Requirements**  

- **Python 3.x** (Recommended: Latest version from [python.org](https://www.python.org/downloads/))  
- **Required Python Packages:**  
  ```plaintext
  pandas
  moviepy
  openpyxl
  ```

---

## **Installation & Setup**  

### **1. Install Python**  
Check if Python is installed by running the following command:  
```bash
python3 --version
```
- If Python is not installed, download and install the latest version from [python.org](https://www.python.org/downloads/).  
- **Important:** During installation, select the option **"Add Python to PATH"** to enable command-line execution.  

---

### **2. Navigate to Your Project Directory**  
Use the `cd` command to move to the directory where the script is stored. Replace `path/to/your/project` with the actual file path.  

#### **On macOS/Linux:**  
```bash
cd ~/path/to/your/project
```
#### **On Windows (Command Prompt):**  
```cmd
cd C:\path\to\your\project
```
#### **On Windows (PowerShell):**  
```powershell
Set-Location "C:\path\to\your\project"
```

#### **Example Usage for External Drives:**  
- **Mac/Linux (Mounted Drive):**  
  ```bash
  cd /Volumes/YourDriveName/ProjectFolder
  ```
- **Windows (Mapped Drive or External Storage):**  
  ```cmd
  cd X:\ProjectFolder
  ```
  *(Replace `X:` with the correct drive letter.)*

---

### **3. (Optional) Install Dependencies**  
To install the required Python packages, run:  
```bash
pip install -r requirements.txt
```
- If using **Python 3.12.5 or later**, use:  
  ```bash
  pip3 install -r requirements.txt
  ```
- **If pip is not recognized**, you may need to add Python and pip to PATH. The easiest fix is reinstalling Python and ensuring **"Add Python to PATH"** is checked during installation.  

⚠ **Note:** This step is optional. The script includes a conditional check and will automatically install any missing packages if needed.  

---

## **Running the Batch Rename Script**  

### **Basic Command:**  
```bash
python batchRename.py --source-folder /path/to/files --pattern "IMG_####"
```
*(Modify `/path/to/files` to the correct location.)*  

---

## **Project Purpose & Benefits**  
This automation script helps to:  
✔ Improve **file organization** and naming consistency  
✔ Reduce **manual workload** by automating renaming processes  
✔ Optimize **storage management** with data analysis  

---

## **Troubleshooting & FAQs**  
- **Python command not recognized?** Ensure Python is installed and added to your system PATH.  
- **Script dependencies missing?** Run `pip install -r requirements.txt` to install missing libraries.  
- **Unexpected errors?** Verify file paths and naming conventions match expected formats.  

---

## **Contact & Contributions**  
For questions, suggestions, or contributions, contact:  
📧 **Crystal Hollis** – `crystaljhollis@gmail.com`  
🔗 [GitHub Profile](https://github.com/crystaljhollis)  

Feel free to submit issues or pull requests for improvements.  

---

## **License**  
MIT License – Free to use, modify, and distribute with attribution.  
