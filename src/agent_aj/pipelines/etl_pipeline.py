# agent_aj/pipelines/etl_pipeline.py
import os
import pandas as pd
from google.cloud import bigquery
from agent_aj import config

class ETLPipeline:
    """Handles loading unstructured data to BigQuery."""
    def __init__(self, project_id: str, dataset_id: str, table_id: str):
        # Ensure project_id is not None before creating client
        if not project_id:
            raise ValueError("GCP_PROJECT_ID is not set. Please check your .env file.")
        self.client = bigquery.Client(project=project_id)
        self.table_ref = self.client.dataset(dataset_id).table(table_id)

    def _parse_unstructured_data(self, file_path: str) -> pd.DataFrame:
        """A simple parser for the sample text file."""
        print(f"Attempting to read data from: {file_path}")
        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"The data file was not found at the specified path: {file_path}. "
                "Please ensure the 'data/travel_deals.txt' file exists in your project root."
            )
        
        with open(file_path, 'r') as f:
            content = f.read()
        
        packages = content.strip().split('\n\n')
        data = []
        for package in packages:
            details = {}
            lines = [line for line in package.split('\n') if line.strip()]
            for line in lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    details[key.strip()] = value.strip()
            if details: # Only add if details were parsed
                data.append(details)
        return pd.DataFrame(data)

    def run(self, data_file_path: str):
        """Executes the ETL pipeline."""
        print("🚀 Starting ETL Pipeline...")
        df = self._parse_unstructured_data(data_file_path)
        
        if df.empty:
            print("⚠️ Warning: No data was parsed from the file. Aborting BigQuery load.")
            return

        print(f"📄 Parsed {len(df)} records from data file.")

        job_config = bigquery.LoadJobConfig(
            write_disposition="WRITE_TRUNCATE", # Overwrite table
            autodetect=True, # Automatically detect schema
        )
        
        try:
            job = self.client.load_table_from_dataframe(
                df, self.table_ref, job_config=job_config
            )
            job.result() # Wait for the job to complete
            print(f"✅ Successfully loaded data to BigQuery table: {self.table_ref.path}")
        except Exception as e:
            print(f"❌ An error occurred during the BigQuery load: {e}")
            print("Please check your GCP authentication and BigQuery permissions.")


if __name__ == '__main__':
    # --- FIX: Build a robust, absolute path to the data file ---
    # This script is in /src/pipelines, so we go up three levels to get to the project root
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    #data_file = os.path.join(project_root, 'data', 'travel_deals.txt')
    data_file = "./src/agent_aj/pipelines/data/travel_deals.txt"
    
    # Example execution
    pipeline = ETLPipeline(
        project_id=config.GCP_PROJECT_ID,
        dataset_id=config.GCP_BIGQUERY_DATASET,
        table_id=config.BQ_TABLE_NAME
    )
    pipeline.run(data_file)
