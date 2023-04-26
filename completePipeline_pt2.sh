#!/bin/bash

# THEN ACTIVATE THE ANOTHER ENVIRONMENT (CONDA OR VENV):

source PATH FOR YOUR ENVIRONMENT

# THEN SET A CONFIGURATION, IF YOU WANT TO OBSERVE THE PROCESS THROUGH UI PANEL:

prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api

# SET gcloud AUTHORIZATION:

gcloud auth login

# SET PROJECT ID, FROM GCP PROJECT ID:

gcloud config set project YOUR PROJECT ID
	
# SETTING BUCKET NAME:

bucket_name="telecomm-YOUR PROJECT ID"

# YOU SHOULD CREATE THESE DIRS AT YOUR CLOUD STORAGE BUCKET, FOR STORING THE DATA LAKE:

echo ""
echo ""
echo "Create the next dirs:"
echo ""
echo "$bucket_name/data/telecomm/csv_gz/crm/"
echo ""
echo "$bucket_name/data/telecomm/csv_gz/dev/"
echo ""
echo "$bucket_name/data/telecomm/csv_gz/rev/"
echo ""
read -p "After creating them, press enter to continue"

# PAUSING TO ALLOW GCP CLOUD STORAGE UPDATE THE SERVERS WITH THE RECENT CREATED DIRS
sleep 20s

# CHECK STATUS FLAG OF THE FOLDERS CREATION
gsutil -q stat gs://$bucket_name/data/telecomm/

# WHILE DIRS AREN'T CREATED, ASK TO USER TO DO IT
while [ $? -eq 1 ];
do
    echo "The dirs were not created"
    echo ""
    echo "Create the next dirs:"
    echo ""
    echo "$bucket_name/data/telecomm/csv_gz/crm/"
    echo ""
    echo "$bucket_name/data/telecomm/csv_gz/dev/"
    echo ""
    echo "$bucket_name/data/telecomm/csv_gz/rev/"
    echo ""
    read -p "After creating them, press enter to continue"
done


# RUN PIPELINE FOR EXTRACT, TRANSFORM AND LOAD TO DATA LAKE:

python3 Pipelines/webToGCS_Pipeline.py


# RUN PIPELINE FOR LOAD EXTERNAL TABLE INTO DATA WAREHOUSE:

python3 Pipelines/GCSToBQ_Pipeline.py


# AFTER PIPELINES FINISHED SUCCESSFULLY, INIT DBT:

dbt init
	
#  THE RUN ALL MODELS:

dbt run

# NOTICE WHEN PIPELINE FINISH

echo ""
echo "<----------------------------------- The Pipeline has finished successfully ----------------------------------->"
echo ""