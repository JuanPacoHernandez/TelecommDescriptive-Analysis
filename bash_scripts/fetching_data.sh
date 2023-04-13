#!/bin/bash

#THIS BASH SCRIPT WILL DOWNLOAD A KAGGLE VIA KAGGLE API, YOU HAVE TO INSTALL KAGGLE PACKAGE FIRST
# USE (ABOVE python3) TO INSTALL KAGGLE PACKAGE: pip3 install kaggle 
kaggle datasets download -d krishnacheedella/telecom-iot-crm-dataset
# CREATE A data/ DIR THAT WILL STORE THE DATA
mkdir data/
# TO UNZIP THE FILE, IF THE FILES ALREADY EXISTS, YOU SHOULD PRESS "y" AND ENTER WHEN ASKED YOU
unzip telecom-iot-crm-dataset.zip
# THEN MOVE THE FILE FROM UNZIPPED FILE TO data/ DIR
mv crm1.csv data/ device1.csv data/ rev1.csv data/
# REMOVE ZIP FILE PREVISOULY DOWNLOADED
rm -r telecom-iot-crm-dataset.zip
# NOTICE WHEN PROCESS FINISH
echo
echo "< ------------------------ The telecom-iot-crm-dataset download has been completed successfully! ------------------------ >"
echo

