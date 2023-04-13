# Descriptive Analyisis for Telecomm customers using Pipelines 

## PROBLEM DESCRIPTION

The main idea of this project is to build an end-to-end data pipeline, according to the Problem statement's project it's needed to build a Dashboard with two tiles, so this Dashboard would uncover historical patterns in consumption habits from IoT customers, this Descriptive Analysis describes the consumers in two simple insights, firstly by the Frequency of customers by their year of birth and by their gender, and secondly by the customer gender Distribution. 

Once the problem statement has been described I can go diving into the dataset and I can say that is composed of three tables, a CRM table with information about non-sensible data customers, an IoT devices table with information about the customers' devices, and a Revenue table with customer's revenue generated by weeks. The dataset is composed of three tables, a CRM table with over 13M of records, and two tables Devices (2.4M records) and Revenues (1.7M records).

Since the Descriptive Analysis only requires historical data about customer age and gender, the CRM table, Fact table, would be enough to describe these consumer features. And, due to the origin of the dataset, is possible to perform the Pipeline periodically with no need of real-time analysis, so I decided to perform Batch Processing.

Nevertheless for not despising the importance of the rest of the Dimension tables (Devices table and Revenue table), non-used in performing the Data Analysis but useful for future Analyses, stored in the Data Warehouse, it is important to ensure Data Integrity for the three tables within a Workflow Orchestration using Infrastructure as Code, that's why this Project covers the use of Terraform (IaC), Spark (PySpark) for Batch Processing and Transformation of data (dbt core), along with GCP storage service (as Data Lake) and BigQuery (as Data Warehouse) to finally crafting a Dashboard in Data studio and adding Portability to the Dashboard with Streamlit tool. For complementing there will use Test to Pipelines Data Ingestions and Transformations.

Now, the stakeholders would be:

- Investors interested in Telecom companies.
- Telecomm service providers companies.
- Government officials for sharing reports with citizens.
- Public interest of the community.
- Journalists working on tech articles.
- Telecomm enthusiatics.


The data consists in three datasets: 

**CRM ATTRIBUTE DESCRIPTION** 
- msisdn  : Unique identification number assigned to each mobile number
- gender  : sex of the customer using the mobile service
- year_of_birth  : year of birth of the customer
- system_status  : indicates the status of the mobile service being used by the customer
- mobile_type  : Customers can choose their service as prepaid or postpaid
- value_segment  : Segmentation based on how well the customer matches the business goals

**IOT DEVICES ATTRIBUTE DESCRIPTION**
- msisdn: Unique identification number assigned to each mobile number
- imei_tac: Unique identification number assigned to the location of the mobile service
- brand_name: The brand of the mobile
- model_name: The model of the mobile
- os_name: The Operating System of the mobile
- os_vendor: The company of the mobile operating system

**REVENUE ATTRIBUTE DESCRIPTION**
- msisdn  : Unique identification number assigned to each mobile number
- week_number : Week number for the particular year
- Revenue_usd : Revenue generated in that week in US dollars

CRM, DEV and REV datasets source: 

[(https://www.kaggle.com/datasets/krishnacheedella/telecom-iot-crm-dataset?resource=download)]

Data sets source for determining the life expectancy of US citizens up to 2020 year:

[(https://data.worldbank.org/indicator/SP.DYN.LE00.IN?locations=US)]

PACKAGES THAT NEED TO BE INSTALLED, IN A CONDA/PYTHON ENVIRONMENT:
- **Prefect**
- **Python above version 3**
- **Spark (PySpark)**
- **gcloud CLI**
- **dbt core with bigquery adapter**

THESE PACKAGES SHOULD BE INSTALLATED WITHIN A ENVIRONMENT LIKE CONDA OR VENV, THEN MAKE SURE TO RUN THE ENVIRONMENT BEFORE RUN THE PIPELINES AND COMMANDS.


## CLOUD

For Clouding service I decided to use GCP, to store the Data Lake I use Cloud Storage creating a Bucket, not forgetting to enable IAM permissions and roles:

- Store Admin
- BigQuery Admin
- Storing objects and environment Admin
- Visualizer

Also the JSON file generated by adding the key to the Service Account associated to the User will be needed, make sure this JSON file would be included to the .gitignore file, avoiding to expose it in Github.

For housing the Data Warehouse, BigQuery was the choice to take advantage of the free credit for first use. Also to leverage BigQuery's Partitioning by and Clustering by to create an optimized table and hence reducing billing when Data Analysts, Data Scientists and Stakeholders need consuming data.



## BATCH DATA INGESTION/WORKFLOW ORCHESTRATION WITH PREFECT (PIPELINE FROM PROCESSING AND INGEST INTO DATA LAKE)

When performing Data ingestion, using Batch Processing, this project use PySpark along with Bash to:

- **Extract** three datasets from Kaggle using Kaggle API (Bash commands)
- **Transform** for cleansing stage using PySpark, and 
- **Load**, using Bash commands, this stage is splitted in two Loads, the first Load is to push the datasets into a Data Lake in a Bucket located in Cloud Storage (GCP), the second Load is to push datasets from Cloud Storage into BigQuery Tables.

The **webToGCS_Pipeline.py** python3 file is a Pipeline to process the datasets in Batches and putting them to a Data Lake in GCP, this file contains the **Extract**, **Transform**, and **Load** to GCP (Data Lake) stages.

This python file uses scripts in Bash to perform fetching data, **fetching_data.sh** download the datasets from Kaggle's API, unzip the datasets and move to a "data" dir, at the end the script removes the downloaded zipped file from Kaggle. After that, this python file perform clean and filter processes over the datasets to finally upload the datasets in a Data Lake in GCP Cloud Storage running a Bash script **uploading_data.sh**.



## DATA WAREHOUSE

For housing the Data Warehouse, BigQuery was the choice to take advantage of the free credit for first use. Also to leverage BigQuery's external tables, the Partitioning by (using dbt core), and the Clustering by (using dbt core) to create an optimized table and hence reducing billing when Data Analysts, Data Scientists and Stakeholders need consuming data. The next IAM permissions and roles should be enabled:

- Store Admin
- BigQuery Admin
- Storing objects and environment Admin
- Visualizer

As I mentioned previously, the second **Load** is to transfer data from GCP Bucket to BigQuery Tables, as external tables, called **external_CRM**, **external_DEV**, and **external_REV** tables through **GCSToBQ_Pipeline.py** file, but before run this python file make sure permissions are allowed for Bash files.


## TRANSFORMATIONS

Remembering that for Dashboard crafting purposes only CRM dataset is enough to perform the two tiles, so by using dbt cloud or dbt core will help to Transformate our CRM external table in a more efficient way, in the dbt model **fact_crm.sql** I include a **Partition** by "year_of_birth" column from CRM table and also I include a **Cluster** by "gender" column, this improve the reading time of the table achieving less billing in GCP. Prior running the **fact_crm.sql** model is mandatory to run **stg_crm.sql** model which it bring the view from an external table, stored at BigQuery after the Loading stage performed by **GCSToBQ_Pipeline.py**. 


## DASHBOARD

The Dashboard was crafted in Looker Studio (before Data Studio):

[(https://lookerstudio.google.com/reporting/59c58893-a921-40c6-a39c-ad224e19e04f)]

I use a Pie chart for describing the **Telecomm customers gender distribution** and a 100% Stacked bar for showing the **Frequency of Telecomm customers by year of birth and by gender**.


## REPRODUCIBILITY

These are the steps to follow to execute the Pipeline, run in terminal:

1.- ALLOW PERMISSIONS TO BASH SCRIPTS INCLUDED IN THE REPO:

`chmod +x bash_scripts/fetching_data.sh bash_scripts/uploading_data.sh bash_scripts/crm_gcs_to_bq.sh bash_scripts/dev_gcs_to_bq.sh bash_scripts/rev_gcs_to_bq.sh`
	

2.- YOU WILL NEED A BUCKET IN GCP ENABLED AND MAKE SURE TO SPECIFY **YOUR BUCKET NAME** WITHIN THE BASH FILES:

- bash_scripts/crm_gcs_to_bq.sh 
- bash_scripts/dev_gcs_to_bq.sh 
- bash_scripts/rev_gcs_to_bq.sh
	

3.- ACTIVATE THE DESIRED ENVIRONMENT (CONDA OR VENV)
	

4.- RUN PREFECT ORION SERVER, BUT FIRST ACTIVATE ANACONDA BASE ENVIRONMENT:

`prefect orion start`


5.- THEN SET A CONFIGURATION, IF YOU WANT TO OBSERVE THE PROCESS THROUGH UI PANEL:

`prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api`


6.- SET gcloud AUTHORIZATION:

`gcloud auth login`


7.- SET PROJECT ID, FROM GCP PROJECT ID:

`gcloud config set project <PROJECT ID>`
	

8.- YOU SHOULD CREATE THESE DIRS AT YOUR CLOUD STORAGE, FOR STORING THE DATA LAKE:

- data/telecomm/csv_gz/crm/
- data/telecomm/csv_gz/dev/
- data/telecomm/csv_gz/rev/


9.- RUN PIPELINE FOR EXTRACT, TRANSFORM AND LOAD TO DATA LAKE:

`python3 Pipelines/webToGCS_Pipeline.py`


10.- RUN PIPELINE FOR LOAD EXTERNAL TABLE INTO DATA WAREHOUSE:

`python3 Pipelines/GCSToBQ_Pipeline.py`


11.- AFTER PIPELINES FINISHED SUCCESSFULLY, INIT DBT:

`dbt init`
	

12.- CONFIGURE WITH THIS REQUIREMENTS WHEN dbt init:

- `bigquery` (This implies that dbt should be installed along with bigquery adapter)
- `service_account` (Specify the path of the JSON file key for Service Account)
- `GCP project id`  (Specify Project's ID)
- `dbt_Analytics_Telecomm`  (suggested dbt dataset name, change if desire)
- `threads = 1`
- `job_execution_timeout_seconds = 300`
- `US` (Desired location or of your preference)


13.- Check if the files required are in the same folder before running dbt:

- **/models/staging/stag_crm.sql**
- **/models/stating/schema.yml**
- **/models/core/fact_crm.sql**
- **/models/core/schema.yml**
- **/dbt_project.yml**


14.- THE RUN ALL MODELS:

`dbt run`
	
	
AT THIS TIME, DATA LAKE HOLDS THE DATASETS FROM KAGGLE API WITHIN THE DIR:

**data/telecomm/csv_gz**

BIGQUERY HOLDS EXTERNAL TABLES:

- **external_CRM**
- **external_DEV**
- **external_REV** 

AND ALSO BIGQUERY HOLDS THE PARTITIONED AND CLUSTERED TABLE FOR CRM TABLE, REMEMBER THAT FOR CRAFTING THE DASHBOARD IT'S ONLY CRM TABLE NEEDED, SO NOW IT IS POSSIBLE TO CRAFT A DASHBOARD WORKING FROM THIS BIGQUERY TABLE:
**fact_crm**

THE **stg_crm** HOLDS A VIEW FROM external_CRM TABLE.



## TESTING STAGE

https://towardsdatascience.com/how-to-test-pyspark-etl-data-pipeline-1c5a6ab6a04b


## USEFUL WEBSITE LINKS:

- EXPORTING GCS TO BIGQUERY:

[(https://cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=es-419)]


- BIGQUERY CONNECTOR WITH SPARK:

[(https://cloud.google.com/dataproc/docs/tutorials/bigquery-connector-spark-example?hl=es-419#pyspark)]


- PARTITION BY IN BIGQUERY:

[(https://cloud.google.com/bigquery/docs/creating-partitioned-tables?hl=es#sql_2)]
[(https://towardsdatascience.com/how-to-use-partitions-and-clusters-in-bigquery-using-sql-ccf84c89dd65)]


- CLUSTERED BY BIGQUERY:

[(https://cloud.google.com/bigquery/docs/creating-clustered-tables?hl=es-419#sql_1)]


- PARTITIONED IN DBT CLOUD:

[(https://docs.getdbt.com/reference/resource-configs/bigquery-configs#partition-clause)]


- CLUSTERRED BY DBT CLOUD:

[(https://docs.getdbt.com/reference/resource-configs/bigquery-configs#clustering-clause)]




