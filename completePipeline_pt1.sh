#!/bin/bash

# MAKE SURE main.tf AND variables.tf FILES ARE IN CURRENT FOLDER BERORE RUNNING terraform

terraform init
terraform plan -var="project=YOUR PROJECT ID"
terraform apply -var="project=YOUR PROJECT ID"


# ALLOW PERMISSIONS TO BASH SCRIPTS INCLUDED IN THE REPO:

chmod +x bash_scripts/fetching_data.sh bash_scripts/uploading_data.sh bash_scripts/crm_gcs_to_bq.sh bash_scripts/dev_gcs_to_bq.sh bash_scripts/rev_gcs_to_bq.sh
	
#  ACTIVATE THE DESIRED ENVIRONMENT (CONDA OR VENV):

source PATH FOR YOUR ENVIRONMENT

# RUN PREFECT ORION SERVER, BUT FIRST ACTIVATE ANACONDA BASE ENVIRONMENT:

prefect orion start