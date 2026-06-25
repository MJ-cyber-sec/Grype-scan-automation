# Grype-scan-automation

What the project is ?

Docker image vulnerability scanning using Grype on client. Instead of running the command one by one to run the grype on each file (.tar) in the folder, me and my senior automates the tasks using bash script and export them to an organized excel file using python.

Why it was built ?
During the first scan, I only thought of scanning the image file one by one then later need to generate the output also on by one, but my senior saw this and tell me that manual scanning was repetitive and error-prone, so this automation was developed to streamline the process for the next one after remediation. We ask claude to generate the bash script to automate the process and python to export from json to excel. 3 times scan.

How it works (the workflow) ?
1. Received .tar files from client
2. run the bash script -> the results in json file at a new folder
3. then export the json file to excel file for each json file using python
4. Final report in excel file

Requirements
Grype installed
Python3
openpyxl library
- the OS environment is Kali Linux

Usage
./grype automate.sh /folder  ###automate.sh is the bash script file, /folder is where the .tar file is contain

ls -lh ###after done check the output to ensure it works and the output of json file exists

python file.py --path result path ###file.py is the python script and --path is where the folder contain the json file and will will create "result" directory on "path" any target path
