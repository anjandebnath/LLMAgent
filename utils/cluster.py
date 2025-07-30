'''
The Clusterer class uses the Extractor to fetch a dataset. 
It then applies the DBSCAN (Density-Based Spatial Clustering of Applications with Noise) algorithm 
to group similar data points together and identify outliers. 
Finally, it labels each data point with its corresponding cluster ID and saves the augmented dataset back to S3.

'''

# Import necessary libraries for data handling, numerical operations, and date/time.
import pandas as pd
import numpy as np
import datetime
import logging
# Basic configuration for the logging module to display INFO level messages.
logging.basicConfig(level=logging.INFO)

# Import boto3 for AWS S3 interaction.
import boto3
# Import StandardScaler for feature normalization and DBSCAN for the clustering algorithm.
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
# Import the Extractor class from the local utils package.
from extractor import Extractor

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# A dictionary holding the default hyperparameters for the DBSCAN model.
# 'eps' is the maximum distance between two samples for one to be considered as in the neighborhood of the other.
# 'min_samples' is the number of samples in a neighborhood for a point to be considered as a core point.
model_params = {
    'eps': 0.3,
    'min_samples': 10,
}

# Definition of the Clusterer class.
class Clusterer:
    """
    A class to perform DBSCAN clustering on data extracted from S3.
    """
    
    # The constructor for the Clusterer class.
    def __init__(
        self, bucket_name: str, 
        file_name: str, 
        model_params: dict = model_params
    ) -> None:
        """
        Initializes the Clusterer.
        :param bucket_name: The S3 bucket where the data is stored.
        :param file_name: The file to be processed.
        :param model_params: A dictionary of parameters for the DBSCAN model.
        """
        # Stores the DBSCAN model parameters.
        self.model_params = model_params
        # Stores the S3 bucket name.
        self.bucket_name = bucket_name
        # Stores the name of the file to be clustered.
        self.file_name = file_name
        
    # The main method that orchestrates the clustering process.
    # It takes a list of strings, which are the column names to be used as features for clustering.
    def cluster_and_label(self, features: list) -> str:
        """
        Extracts data, scales features, runs DBSCAN, labels the data, and saves it to S3.
        :param features: A list of column names to use for clustering.
        """
        # Creates an instance of the Extractor to fetch the data.
        extractor = Extractor(self.bucket_name, self.file_name)
        # Calls the extract_data method to get the DataFrame.
        df = extractor.extract_data()
        # Creates a new DataFrame containing only the feature columns specified for clustering.
        df_features = df[features]
        # Initializes StandardScaler and applies it to the features. This scales the data to have a mean of 0 and a standard deviation of 1.
        df_features = StandardScaler().fit_transform(df_features)
        # Initializes the DBSCAN model using the parameters stored in self.model_params (** unpacks the dictionary into keyword arguments).
        # The .fit() method computes DBSCAN clustering from features.
        db = DBSCAN(**self.model_params).fit(df_features)

        # The following lines are for analyzing the results but are not strictly necessary for labeling.
        # Creates a boolean mask, initially all False, with the same shape as the labels array.
        ##core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
        # Sets the mask to True for indices corresponding to core samples identified by DBSCAN.
        ##core_samples_mask[db.core_sample_indices_] = True
        # Retrieves the cluster labels for each data point. Outliers are given the label -1.
        labels = db.labels_

        # Adds a new 'label' column to the original DataFrame, containing the cluster labels.
        df['label'] = labels
        
        # Gets the current date and formats it as YYYYMMDD to create a unique filename.
        date = datetime.datetime.now().strftime("%Y%m%d")

        output_key = f"clustered_data_{date}.json"
        # Creates an S3 client.
        boto3.client('s3').put_object(
            # Converts the labeled DataFrame to a JSON string in a record-oriented format.
            Body=df.to_json(orient='records'), 
            # Specifies the target S3 bucket.
            Bucket=self.bucket_name, 
            # Defines the name of the new file, including the date.
            Key=output_key
        )
        return output_key

# This block runs only when the script is executed directly
if __name__ == "__main__":
    # Read configuration from environment variables
    bucket = os.getenv("S3_BUCKET")
    raw_file = os.getenv("RAW_DATA_FILENAME")

    # Define the features to use for clustering.
    # These are the actual numerical columns from simulate.py
    features_to_cluster = ['ride_dist', 'ride_time', 'ride_speed']
    
    print(f"Attempting to cluster {raw_file} from bucket {bucket}...")
    
    # Instantiate and run the clusterer
    clusterer = Clusterer(bucket_name=bucket, file_name=raw_file)
    output_filename = clusterer.cluster_and_label(features=features_to_cluster)
    
    print(f"Clustering complete. Labeled data saved to S3 as: {output_filename}")
      

        