# src/pipelines/feature_pipeline.py
import pandas as pd
from langchain_community.vectorstores import Qdrant
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from google.cloud import bigquery
from agent_aj import config

class FeaturePipeline:
    """Handles creating and storing vector embeddings in Qdrant."""
    def __init__(self):
        self.bq_client = bigquery.Client(project=config.GCP_PROJECT_ID)
        self.embeddings = OllamaEmbeddings(
            model=config.EMBEDDING_MODEL, 
            base_url=config.OLLAMA_BASE_URL
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
        )

    def _fetch_data_from_bigquery(self) -> pd.DataFrame:
        """Fetches the raw data from our BigQuery table."""
        query = f"""
            SELECT *
            FROM `{config.GCP_PROJECT_ID}.{config.GCP_BIGQUERY_DATASET}.{config.BQ_TABLE_NAME}`
        """
        print("🔍 Fetching data from BigQuery...")
        return self.bq_client.query(query).to_dataframe()

    def run(self):
        """Executes the feature pipeline."""
        print("🚀 Starting Feature Pipeline...")
        df = self._fetch_data_from_bigquery()
        
        # Combine relevant fields into a single document for embedding
        df['document'] = "Destination: " + df['Destination'] + ". Description: " + df['Description']
        
        # Chunking
        texts = self.text_splitter.split_text(" ".join(df['document']))
        print(f"📄 Split data into {len(texts)} chunks.")

        # Create and store embeddings in Qdrant
        print(f"🤖 Generating embeddings and storing in Qdrant collection: '{config.QDRANT_COLLECTION_NAME}'...")
        Qdrant.from_texts(
            texts,
            self.embeddings,
            host=config.QDRANT_HOST,
            port=config.QDRANT_PORT,
            collection_name=config.QDRANT_COLLECTION_NAME,
            force_recreate=True, # Overwrite collection
        )
        print("✅ Feature pipeline completed successfully!")

if __name__ == '__main__':
    pipeline = FeaturePipeline()
    pipeline.run()