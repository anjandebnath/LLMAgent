# agent_aj/data_storage.py
# This script demonstrates Encapsulation.

from pymongo import MongoClient
from typing import List, Dict, Any

# Concept: Encapsulation
# The DataStorer class encapsulates the logic for interacting with MongoDB.
# The user of this class doesn't need to know the details of how the
# connection is made or how data is inserted. They just call the 'store' method.
# The internal state (client, db) is managed within the class.
class DataStorer:
    """A class to handle storing data in MongoDB."""

    def __init__(self, mongo_uri: str, db_name: str):
        """
        Initializes the DataStorer with MongoDB connection details.

        Args:
            mongo_uri: The connection string for MongoDB.
            db_name: The name of the database to use.
        """
        # Concept: Instance Attributes
        # These attributes hold the state for each instance of the class.
        self.mongo_uri = mongo_uri
        self.db_name = db_name
        self.client = None
        self.db = None

    # Concept: Context Manager
    # The '__enter__' and '__exit__' methods allow this class to be used
    # with a 'with' statement. This ensures that the database connection
    # is automatically opened and closed, which is a best practice for
    # managing resources.
    def __enter__(self):
        """Opens the MongoDB connection."""
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.db_name]
        print("MongoDB connection opened.")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Closes the MongoDB connection."""
        if self.client:
            self.client.close()
            print("MongoDB connection closed.")

    def store(self, collection_name: str, data: List[Dict[str, Any]]):
        """

        Stores a list of documents in a specified collection.

        Args:
            collection_name: The name of the collection to store data in.
            data: A list of dictionary objects to be stored as documents.
        """
        if not self.db:
            raise ConnectionError("Database connection is not open. Use within a 'with' statement.")

        if not data:
            print("No data provided to store.")
            return

        collection = self.db[collection_name]
        # Concept: Error Handling
        # A try...except block is used to gracefully handle potential errors
        # during the database insertion process.
        try:
            result = collection.insert_many(data)
            print(f"Successfully inserted {len(result.inserted_ids)} documents into '{collection_name}'.")
        except Exception as e:
            print(f"An error occurred while storing data: {e}")

