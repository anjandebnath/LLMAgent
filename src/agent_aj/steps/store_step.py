# agent_aj/steps/store_step.py
# This script defines the ZenML step for storing data.

from zenml import step
from typing import List, Dict, Any
from ..data_storage import DataStorer

@step
def store_data_in_mongodb(
    data: List[Dict[str, Any]],
    mongo_uri: str = "mongodb://localhost:27017/",
    db_name: str = "agent_aj_db",
    collection_name: str = "unstructured_posts"
) -> None:
    """
    A ZenML step that stores data in a MongoDB collection.

    Args:
        data: The data to be stored (list of dictionaries).
        mongo_uri: The connection URI for MongoDB.
        db_name: The name of the database.
        collection_name: The name of the collection.
    """
    print("--- Starting Store Step ---")
    # Using the DataStorer with a 'with' statement ensures the connection
    # is properly managed.
    try:
        with DataStorer(mongo_uri, db_name) as storer:
            storer.store(collection_name, data)
        print("--- Store Step Finished ---")
    except Exception as e:
        print(f"Failed to execute store step: {e}")
