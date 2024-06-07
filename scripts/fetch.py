import requests
import json
import time
import boto3
import os
from datetime import datetime

def load_config():
    with open('../config/config.json', 'r') as file:
        config = json.load(file)
    return config

def fetch_weather_data(api_call):
    response = requests.get(api_call)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return None
    
def save_raw_data(data, output_dir='data/raw'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"{output_dir}/weather_{timestamp}.json"
    with open(filename, 'w') as file:
        json.dump(data, file)
    print(f"Raw data saved locally to {filename}")

def upload_to_s3(data, bucket_name, key, region):
    s3_client = boto3.client('s3', region_name=region)
    try:
        s3_client.put_object(Body=json.dumps(data), Bucket=bucket_name, Key=key)
        print(f"Data uploaded to S3 bucket '{bucket_name}' with key '{key}'")
    except Exception as e:
        print(f"Failed to upload data to S3: {e}")

def main():
    config = load_config()
    api_call = config['api_call']
    s3_bucket = config['s3']['bucket']
    s3_key_template = config['s3']['key']
    region = config['s3']['region']
    interval = config['interval']

    while True:
        weather_data = fetch_weather_data(api_call)
        if weather_data:
            save_raw_data(weather_data)  # Save raw data locally
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            s3_key = s3_key_template.format(timestamp=timestamp)
            upload_to_s3(weather_data, s3_bucket, s3_key, region)
        time.sleep(interval)

if __name__ == "__main__":
    main()
