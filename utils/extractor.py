"""
The Extractor class is a simple, focused utility responsible for one task: 
connecting to an AWS S3 bucket, retrieving a specified JSON file, and loading its contents into a pandas DataFrame. 
This encapsulates the data extraction logic, making it reusable across different parts of the application.

"""

# Import the pandas library, essential for data manipulation and analysis, aliased as pd.
import pandas as pd
# Import the boto3 library, which is the AWS SDK for Python, used to interact with AWS services like S3.
import boto3

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Definition of the Extractor class.
class Extractor:
    """
    A class to extract data from a JSON file stored in an AWS S3 bucket.
    """
    
    # The constructor method, called when a new Extractor object is created.
    # It requires a bucket_name (string) and a file_name (string).
    # Type hints (-> None) indicate that this method doesn't return any value.
    def __init__(self, bucket_name: str, file_name: str) -> None:
        """
        Initializes the Extractor with S3 bucket and file details.
        :param bucket_name: The name of the AWS S3 bucket.
        :param file_name: The key (path) to the JSON file within the bucket.
        """
        # Stores the provided bucket name as an instance variable.
        self.bucket_name = bucket_name
        # Stores the provided file name as an instance variable.
        self.file_name = file_name

    # A method to perform the data extraction.
    # It is type-hinted to return a pandas DataFrame.
    def extract_data(self) -> pd.DataFrame:
        """
        Connects to S3, retrieves the specified file, and loads it into a pandas DataFrame.
        :return: A pandas DataFrame containing the data from the JSON file.
        """
        # Creates a low-level S3 client object using boto3. This client is used to make API requests to S3.
        s3 = boto3.client('s3')
        # Calls the get_object method on the S3 client to retrieve the file.
        # It specifies the Bucket and the Key (file name) to identify the object.
        obj = s3.get_object(Bucket=self.bucket_name, Key=self.file_name)
        # Uses pandas' read_json function to parse the JSON data.
        # obj['Body'] is a streaming body object from the S3 response, which pandas can read directly.
        df = pd.read_json(obj['Body'])
        # Returns the newly created DataFrame.
        return df

# This block runs only when the script is executed directly
if __name__ == "__main__":
    # Read configuration from environment variables
    bucket = os.getenv("S3_BUCKET")
    raw_file = os.getenv("RAW_DATA_FILENAME")
    
    print(f"Attempting to extract {raw_file} from bucket {bucket}...")
    
    # Instantiate and run the extractor
    extractor = Extractor(bucket_name=bucket, file_name=raw_file)
    data = extractor.extract_data()
    
    print("Successfully extracted data. First 5 rows:")
    print(data.head())
