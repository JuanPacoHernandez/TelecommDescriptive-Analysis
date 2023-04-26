#!/bin/bash

# TO CREATE AN EXTERNAL TABLE 
# 1.- CREATE A TABLE DEF TO MAKE, BASED ON THIS, THE EXTERNAL TABLE

bq mkdef --source_format=CSV \
	gs://telecomm-YOUR PROJECT ID/data/telecomm/csv_gz/rev/*.csv.gz > rev_def

# 2.- CREATE EXTERNAL TABLE BASED ON TABLE DEF, DEFINING DATASET.NAME_OF_TABLE, AND DEFINE A SCHEMA
bq mk --table \
  --external_table_definition=rev_def \
  dbt_Analytics_Telecomm.external_REV \
  msisdn:STRING,week_number:INTEGER,revenue_usd:NUMERIC










