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

The **webToGCS_Pipeline.py** python3 file is a Pipeline to process the datasets in Batches and putting them to a Data Lake (called **telecomm-<YOUR PROJECT ID>**) in GCP, this file contains the **Extract**, **Transform**, and **Load** to GCP (Data Lake) stages.

This python file uses scripts in Bash to perform fetching data, **fetching_data.sh** download the datasets from Kaggle's API, unzip the datasets and move to a "data" dir, at the end the script removes the downloaded zipped file from Kaggle. After that, this python file perform clean and filter processes over the datasets to finally upload the datasets in a Data Lake in GCP Cloud Storage running a Bash script **uploading_data.sh**.



## DATA WAREHOUSE

For housing the Data Warehouse, BigQuery was the choice to take advantage of the free credit for first use. Also to leverage BigQuery's external tables, the Partitioning by (using dbt core), and the Clustering by (using dbt core) to create an optimized table and hence reducing billing when Data Analysts, Data Scientists and Stakeholders need consuming data. The Data Warehouse is called **dbt_Analytics_Telecomm**.

The next IAM permissions and roles should be enabled:

- Store Admin
- BigQuery Admin
- Storing objects and environment Admin
- Visualizer

As I mentioned previously, the second **Load** is to transfer data from GCP Bucket to BigQuery Tables, as external tables, called **external_CRM**, **external_DEV**, and **external_REV** tables through **GCSToBQ_Pipeline.py** file, but before run this python file make sure permissions are allowed for Bash files.


## TRANSFORMATIONS

Remembering that for Dashboard crafting purposes only CRM dataset is enough to perform the two tiles, so by using dbt cloud or dbt core will help to Transformate our CRM external table in a more efficient way, in the dbt model **fact_crm.sql** I include a **Partition** by "year_of_birth" column from CRM table and also I include a **Cluster** by "gender" column, this improve the reading time of the table achieving less billing in GCP. Prior running the **fact_crm.sql** model is mandatory to run **stg_crm.sql** model which it bring the view from an external table, stored at BigQuery after the Loading stage performed by **GCSToBQ_Pipeline.py**. 


## DASHBOARD

The Dashboard was crafted in Looker Studio (before Data Studio), the Dashboard will be available as soon as Free Credit would be consumed:

[(https://lookerstudio.google.com/reporting/59c58893-a921-40c6-a39c-ad224e19e04f)]

I use a Pie chart for describing the **Telecomm customers gender distribution** and a 100% Stacked bar for showing the **Frequency of Telecomm customers by year of birth and by gender**.


## REPRODUCIBILITY

PREVIOUS REQUIREMENTS BEFORE RUN THE PIPELINE:

1.- Specify **YOUR PROJECT ID** within those files in the indicated line number:

- **variables.tf** (LINE 6)
- **bash_scripts/crm_gcs_to_bq.sh** (LINE 7)
- **bash_scripts/dev_gcs_to_bq.sh** (LINE 7)
- **bash_scripts/rev_gcs_to_bq.sh** (LINE 7)
- **completePipeline_pt1.sh** (LINE 6)
- **completePipeline_pt1.sh** (LINE 7)
- **completePipeline_pt2.sh** (LINE 17)
- **completePipeline_pt2.sh** (LINE 21)

2.- Specify **YOUR REGION** within those files in the indicated line number:

- **variables.tf** (LINE 11)

3.- Specify the **PATH FOR YOUR ENVIRONMENT** within those files in the indicated line number:

- **completePipeline_pt1.sh** (LINE 16)
- **completePipeline_pt2.sh** (LINE 5)

4.- Download your key Service Account JSON file in the same directory where files from repo were cloned


### PIPELINE DETAILS:

There are two files to accomplish the whole Pipeline, **completePipeline_pt1.sh** and **completePipeline_pt2.sh**. First of all, grant permissions to those files:

`chmod +x completePipeline_pt1.sh completePipeline_pt2.sh`

Then run it in terminal, **pay attention when Terraform process validations ocurrs, like typing yes when asking**:

`./completePipeline_pt1.sh`

This previous part of the Pipeline will execute up to Prefect framework, so when you can see the Prefect Orion interface in Terminal then run the second part of the Pipeline in another terminal:

`./completePipeline_pt2.sh`

Next, allow permissions to Google Cloud SDK Authentications in the WebBrowser tab.

Then, you will be asked to **create** three dirs at your Cloud Storage Bucket:

- telecomm-**YOUR PROJECT ID**/data/telecomm/csv_gz/crm/
- telecomm-**YOUR PROJECT ID**/data/telecomm/csv_gz/dev/
- telecomm-**YOUR PROJECT ID**/data/telecomm/csv_gz/rev/

Create them to continue.

Next, you will be asked for configuring dbt init parameters:

- `bigquery` (This implies that dbt should be installed along with bigquery adapter)
- `service_account` (Specify the path of the JSON key file for Service Account)
- `GCP project id`  (Specify Project's ID)
- `dbt_Analytics_Telecomm`  (suggested dbt dataset name)
- `threads = 1`
- `job_execution_timeout_seconds = 300`
- `US` (Desired location or of your preference)


Once the part 2 of the Pipeline finish, the Data Lake holds the Datasets in dir:

**telecomm-**YOUR PROJECT ID**/data/telecomm/csv_gz**

and also Data Warehouse holds the external tables:

- **external_CRM**
- **external_DEV**
- **external_REV** 

Data Warehouse also holds the fact table (Partitioned and Clustered):

**fact_crm**

**stg_crm** (VIEW FROM external_CRM TABLE)

Now you can create the Dashboard in Looker Studio, known before s Data Studio.

Once Dashboard was crafted, then destroy all terraform resources, avoiding undesired billings, by runnning in terminal:

`terraform destroy`



## TESTING STAGE

Adding test stage to the project by **test_GCSToBQ_Pipeline.py** and **test_webToGCS_Pipeline.py**


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

- TESTING PYSPARK ETL DATA PIPELINES:

[(https://towardsdatascience.com/how-to-test-pyspark-etl-data-pipeline-1c5a6ab6a04b)]




