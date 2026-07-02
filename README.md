# Grype-scan-automation

## What is this?
A automation tool for Docker image vulnerability scanning using Grype. Instead of running Grype manually on each `.tar` file one by one, this automates the scanning process for an entire folder and exports the findings into an organised Excel file using Python.

## Background
During a real client engagement, multiple Docker image files needed to be scanned across 3 remediation cycles. In the first scan, images were scanned one by one and output generated manually — which was repetitive and error-prone. My senior identified this and suggested automating the process for subsequent scans. The Bash script and Python export script were developed by Claude to streamline this for the second and third scans.

## How it works
1. Receive `.tar` image files from client
2. Run the Bash script — scans all `.tar` files in the target folder and saves each result as a `.json` file in a new `results/` folder
3. Run the Python script — converts each `.json` file into an organised Excel sheet
4. Final output is a structured Excel report with vulnerability findings

## Requirements
- Kali Linux (development environment)
- [Grype] (https://github.com/anchore/grype) installed
- Python 3
- openpyxl ('pip install openpyxl')

## Usage
#Step 1 - Run Grype scan on all .tar files in target folder
[command]

#Step 2 - Verify JSON output files were created
ls -lh

#Step 3 - Export JSON results to Excel
[command]

## Output
Each `.json` scan result is exported as an organised Excel file containing vulnerability findings including vulnerability ID, severity, description, affected package, package version, fix state, and references.
