#!/bin/bash

# TO CREATE AN EXTERNAL TABLE 
# 1.- CREATE A TABLE DEF TO MAKE, BASED ON THIS, THE EXTERNAL TABLE

bq mkdef --source_format=CSV \
	gs://<YOUR BUCKET NAME>/data/telecomm/csv_gz/crm/*.csv.gz > crm_def

# 2.- CREATE EXTERNAL TABLE BASED ON TABLE DEF, DEFINING DATASET.NAME_OF_TABLE, AND DEFINE A SCHEMA
bq mk --table \
  --external_table_definition=crm_def \
  dbt_Analytics_Telecomm.external_CRM \
  msisdn:STRING,gender:STRING,year_of_birth:INTEGER,system_status:STRING,mobile_type:STRING,value_segment:STRING










