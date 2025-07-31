# ML vs LLM
As ML engineers who want to interact with LLMs, and foundation models in general, is that we can no longer assume we have access to
the `model artifact`, the `training data`, or `testing data`. 
We have to instead treat the model as a third-party service that we should call out to for consumption. Luckily, there are many tools and techniques for implementing this.

LangChain  provides a wide variety of functionality that is useful when dealing with NLP and text-based applications
more generally. 
For example, there are utilities for text splitting, working
with vector databases, document loading and retrieval, and conversational state persistence, among others. 

### Poetry commands
1. Initialize a Poetry project (if not already a Poetry project): `poetry init`
2. Create a virtual environment: Poetry automatically creates a virtual environment when you run: `poetry install`
3. Activate the virtual environment: To activate the virtual environment, run: `poetry shell`
4. To see the path of the current virtual environment, use: `poetry env info`



## Project goal

    Built an ETML pipeline that takes in some taxi ride data, 
    clusters this based on ride distance and time, and then 
    performs text summarization on some contextual information using an LLM

### Output
![alt text](image-2.png)

1. I want to be given clear `labels of anomalous rides` that have anomalously `long ride times `or `distances`
so that I can perform further analysis and modeling on the volume of anomalous rides.
2. I want to be provided with a `summary of relevant textual data` 
so that I can do further analysis and modeling on the reasons for some rides being anomalous.
3. I want all `output data sent to a central location, preferably in the cloud`, 
so that I can easily build dashboards.
4. I would like to see the output data for the `previous day’s rides every morning` 
so that I can  provide an update to the logistics managers

The requirements for our problem have stipulated that we have `relatively small datasets` 
that need to be `processed in batches` every day, first with some kind of clustering or anomaly detection
algorithm before further analysis using an LLM. 

    Data storage and interface options: `AWS S3`
    Modeling part with small data set: `Scikit-learn`
    Text summarization component: `GPT-X models from OpenAI`
    Manage our scheduling: `Airflow`


## Technical Specification
we will actually perform the ETML process twice: 
1. Once for the clustering component and
2. Once for the text summarization. 

`Doing it this way means that we can use intermediary storage in between the steps, in this case, AWS S3 again, in
order to introduce some resiliency into the system. This is so because if the second step fails, it doesn’t mean the first step’s processing is lost.` 

## AirFlow

### How advanced Airflow features helps in ELML process
Good DAG design practices:
#### 1. Embody separation of concerns for your tasks:
At the level of Airflow DAGs we can embody this principle by ensuring our DAGs are built of tasks that have one clear job to do in each case. So, in this example we clearly have the “extract,” “transform,” “ML,” and “load” stages, for which it makes sense to have specific tasks in each case. 
##### Advantage: 
This also helps us to create good control flows and error handling.

#### 2. Use retries:
An important aspect of this is the concept of “retries,” which tells the task to, you guessed it, try the process again if there is a failure. You can also introduce delays between retries and even exponential backoff, which is when your retries have increasing time delays between them. 

#### 3. Mandate idempotency in your DAGs:
Idempotency is the quality of code that returns the same result when run multiple times on the same inputs. 
The challenge for an EMTL application is that we obviously have ML models, for example,
ML models in scikit-learn or neural networks in PyTorch.


#### Configuring Airflow using Docker-Compose 
![alt text](image.png)


#### Configuring Airflow in Python environment


1. To install Apache Airflow using pip within a Poetry Python project while maintaining Poetry's virtual environment, you need to ensure that pip installs Airflow into the Poetry-managed virtual environment.
Verify the active environment: Run: `which pip`
/Users/anjandebnath/Library/Caches/pypoetry/virtualenvs/agent-aj-lR4vpAra-py3.11/bin/pip

2. Typical command to install Airflow from scratch in a reproducible way from PyPI looks like below:
pip install apache-airflow==3.0.0 --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-3.0.0/constraints-3.11.txt"

3. Check install: airflow version
4. Apache Airflow requires a directory to store configuration files, logs, and other data. Set the AIRFLOW_HOME variable to specify this directory.

###### For standalone usage
https://github.com/apache/airflow/blob/main/INSTALLING.md

https://medium.com/@diveshkumarchordia/%EF%B8%8F-getting-started-with-apache-airflow-3-x-a-chronological-troubleshooting-guide-fd22ed755c03

    export AIRFLOW_HOME=~/airflow
    mkdir -p $AIRFLOW_HOME

##### For Custom usage 
https://medium.com/orchestras-data-release-pipeline-blog/installing-and-configuring-apache-airflow-a-step-by-step-guide-5ff602c47a36

Replace `~/airflow` with your preferred directory.
- `export AIRFLOW_HOME=/Users/anjandebnath/Documents/PythonWorkspace/Agent-AJ/airflow/docker`
- `mkdir -p $AIRFLOW_HOME`

- Persist the environment variable: Add the AIRFLOW_HOME variable to your shell configuration (e.g., ~/.bashrc, ~/.zshrc, or ~/.bash_profile on macOS) to make it permanent:
- Add this to your shell configuration (e.g., ~/.bashrc or ~/.zshrc) to persist across sessions:
echo 'export AIRFLOW_HOME=/Users/anjandebnath/Documents/PythonWorkspace/Agent-AJ/airflow/docker' >> ~/.bashrc
source ~/.bashrc

5. Initialize the metastore: `airflow db migrate`
6. Api server: `airflow api-server`  [http://localhost:8080/]
7. Schedular: `airflow scheduler`

#### Run the Dags Report 
`airflow dags report`

#### Forces Airflow to re-read your DAG files and update them in the database.
`airflow dags reserialize`

#### Run the Dag 
1. Check for error: python $AIRFLOW_HOME/dags/sample_dag.py
2. `airflow dags list `
3. `airflow dags trigger sample_dag`

![alt text](image-1.png)


## AWS 

1. check AWS CLI version: aws --version
2. check AWS credetials: aws configure list

#### Add Dependencies with Poetry:
    poetry add python-dotenv pandas boto3 scikit-learn openai


### project Component

1. Simulation (simulate.py): Generates a fake dataset of taxi rides, including numerical data (distance, speed) and contextual text data (news, weather, traffic). This script is the starting point for the entire pipeline.

`poetry run python simulate.py`
- This command will create a new JSON file in a data directory (e.g., ../data/taxi-rides-20250730.json). This file is the raw, unprocessed source data for the entire pipeline.

1.1. Upload the Raw Data to S3
`aws s3 cp ../data/taxi-rides-20250730.json s3://aj-etml-data/source/raw_data.json`
- You can now log in to your AWS S3 console to see that the raw_data.json file exists in the correct location (s3://your-test-bucket-name/source/).


2. Extraction (extractor.py): This is a reusable utility class that connects to an AWS S3 bucket to fetch a specified data file. It's used by other scripts to get the data they need to process.

`poetry run python extractor.py`
- This will extract the data and print the first 5 rows of the DataFrame to your console.


3. Clustering (cluster.py): This script takes the raw taxi ride data, uses the DBSCAN machine learning algorithm to find groups (clusters) of similar rides, and identifies outliers (rides that don't fit any pattern). It then saves this newly labeled data back to S3.

`poetry run python cluster.py`
- This will run the clustering process and print a confirmation message upon saving the new file to S3.


4. Summarization (summarize.py): This final script takes the clustered data and uses the OpenAI API to generate a human-readable summary for each of the outlier rides identified in the previous step. The final, enriched dataset is then saved to S3.

`poetry run python summarize.py`
- This will run the summarization process on the clustered file and print a confirmation message.


