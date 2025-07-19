# src/config.py
import os
from dotenv import load_dotenv
import sys

print("--- Starting Configuration Loading ---")

# Determine the project root directory
# This assumes your script is run from the project root where .env is located
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#dotenv_path = os.path.join(project_root, '.env')
dotenv_path = "./src/agent_aj/.env"

# Explicitly load the .env file from the project root
if os.path.exists(dotenv_path):
    print(f"✅ Found .env file at: {dotenv_path}")
    load_dotenv(dotenv_path=dotenv_path)
else:
    print(f"⚠️ WARNING: .env file not found at {dotenv_path}. Make sure it's in the project root.")
    sys.exit(1) # Exit if .env is missing, as it's critical

# --- Environment ---
APP_ENV = os.getenv("APP_ENV", "development")

# --- LLM & Embeddings ---
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
EMBEDDING_MODEL = "mistral"
LLM_MODEL = "mistral"

# --- Vector Store ---
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
QDRANT_COLLECTION_NAME = "travel_packages"

# --- Data Stores ---
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
GCP_BIGQUERY_DATASET = os.getenv("GCP_BIGQUERY_DATASET")
BQ_TABLE_NAME = "packages"
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# --- DIAGNOSTIC PRINTS ---
print(f"Project ID from env: {GCP_PROJECT_ID}")
print(f"Credentials Path from env: {GOOGLE_APPLICATION_CREDENTIALS}")

if GOOGLE_APPLICATION_CREDENTIALS:
    if os.path.exists(GOOGLE_APPLICATION_CREDENTIALS):
        print(f"✅ Credentials file check PASSED. File exists at: {GOOGLE_APPLICATION_CREDENTIALS}")
    else:
        print(f"❌ Credentials file check FAILED. File NOT FOUND at: {GOOGLE_APPLICATION_CREDENTIALS}")
        print("--- Please verify the path in your .env file is correct. ---")
else:
    print("❌ GOOGLE_APPLICATION_CREDENTIALS environment variable is not set.")

print("--- Configuration Loading Finished ---")


# --- Agent Tools ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

# --- Experiment Tracking ---
COMET_API_KEY = os.getenv("COMET_API_KEY")
COMET_WORKSPACE = os.getenv("COMET_WORKSPACE")
COMET_PROJECT_NAME = os.getenv("COMET_PROJECT_NAME")
