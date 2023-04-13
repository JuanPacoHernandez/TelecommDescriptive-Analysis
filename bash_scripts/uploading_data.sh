#!/bin/bash

# THIS BASH SCRIPT UPLOAD THE DATA FROM DIR "data/csv_gz" TO DIR IN GCS "data/telecomm"
gsutil -m cp -r data/csv_gz gs://prefect-de-zoomcamp-jfcohdz/data/telecomm

# NOTICE WHEN INGESTION FINISH
echo
echo "< ----------------- All crm, dev and rev csv files have been loaded to Data Lake (GCS) successfully ---------------- >"
echo
