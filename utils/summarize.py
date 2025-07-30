from extractor import Extractor
from textwrap import dedent
import datetime
import openai
import boto3
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# The new OpenAI library uses an instantiated client.
# It automatically reads the OPENAI_API_KEY from environment variables.
client = openai.OpenAI()

class LLMSummarizer:
    # ... (class code remains the same as in the documentation)
    def __init__(self, bucket_name: str, file_name: str) -> None:
        self.bucket_name = bucket_name
        self.file_name = file_name

    def summarize(self) -> str:
        extractor = Extractor(self.bucket_name, self.file_name)
        df = extractor.extract_data()
        df['summary'] = ''
        
        df['prompt'] = df.apply(lambda x: self.format_prompt(x['news'], x['weather'], x['traffic']), axis=1)
        df.loc[df['label']==-1, 'summary'] = df.loc[df['label']==-1, 'prompt'].apply(lambda x: self.generate_summary(x))
        
        date = datetime.datetime.now().strftime("%Y%m%d")
        output_key = f"clustered_summarized_{date}.json"
        
        boto3.client('s3').put_object(
            Body=df.to_json(orient='records'), 
            Bucket=self.bucket_name, 
            Key=output_key
        )
        return output_key
    
    def format_prompt(self, news: str, weather: str, traffic: str) -> str:
        # ... (method remains the same)
        prompt = dedent(f'''
            The following information describes conditions relevant to taxi journeys through a single day in Glasgow, Scotland.

            News: {news}
            Weather: {weather}
            Traffic: {traffic}

            Summarise the above information in 3 sentences or less.
            ''')
        return prompt

    def generate_summary(self, prompt: str) -> str:
        # This function is updated for openai version >= 1.0.0
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"An error occurred with the OpenAI API: {e}")
            return "Could not generate summary due to an API error."

# This block runs only when the script is executed directly
if __name__ == "__main__":
    # Read configuration from environment variables
    bucket = os.getenv("S3_BUCKET")
    # IMPORTANT: This script uses the output from the clusterer
    clustered_file = os.getenv("CLUSTERED_DATA_FILENAME")
    
    print(f"Attempting to summarize {clustered_file} from bucket {bucket}...")
    
    # Instantiate and run the summarizer
    summarizer = LLMSummarizer(bucket_name=bucket, file_name=clustered_file)
    output_filename = summarizer.summarize()
    
    print(f"Summarization complete. Final data saved to S3 as: {output_filename}")
