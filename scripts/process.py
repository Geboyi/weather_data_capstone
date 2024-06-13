import json
import requests
import boto3
import os
from datetime import datetime

def load_config():
    with open('./config/config.json', 'r') as file:
        config = json.load(file)
    return config

def fetch_weather_data(api_call):
    response = requests.get(api_call)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return None

def process_weather_data(raw_data):
    try:
        print(f"Raw data received for processing: {raw_data}")
        processed_data = {
            'temperature': raw_data['main']['temp'],
            'humidity': raw_data['main']['humidity'],
            'weather': raw_data['weather'][0]['description'],
            'timestamp': raw_data['dt']
        }
        return processed_data
    except KeyError as e:
        print(f"Missing key in raw data: {e}")
        return None

def save_processed_data(processed_data, output_dir='data/processed'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    filename = f"{output_dir}/weather_{processed_data['timestamp']}.json"
    with open(filename, 'w') as file:
        json.dump(processed_data, file)
    print(f"Processed data saved locally to {filename}")
    return filename

def upload_to_s3(file_path, bucket_name, key, region):
    s3_client = boto3.client('s3', region_name=region)
    try:
        s3_client.upload_file(file_path, bucket_name, key)
        print(f"Processed data uploaded to S3 bucket '{bucket_name}' with key '{key}'")
    except Exception as e:
        print(f"Failed to upload processed data to S3: {e}")

def main():
    config = load_config()
    api_call = config['api_call']
    s3_bucket = config['s3']['bucket']
    s3_region = config['s3']['region']
    s3_key_processed_template = config['s3']['key1']
    
    raw_data_dir = 'data/raw'
    processed_data_dir = 'data/processed'
    
    # Ensure the directories exist
    if not os.path.exists(raw_data_dir):
        os.makedirs(raw_data_dir)
    if not os.path.exists(processed_data_dir):
        os.makedirs(processed_data_dir)

    # Fetch weather data from the API
    weather_data = fetch_weather_data(api_call)
    if weather_data:
        # Save raw data locally (optional)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        raw_data_file = f"{raw_data_dir}/weather_{timestamp}.json"
        with open(raw_data_file, 'w') as file:
            json.dump(weather_data, file)
        print(f"Raw data saved locally to {raw_data_file}")
        
        # Process the raw data
        processed_data = process_weather_data(weather_data)
        if processed_data:
            # Save processed data locally
            processed_file_path = save_processed_data(processed_data, processed_data_dir)
            
            # Upload processed data to S3
            s3_key_processed = s3_key_processed_template.format(timestamp=processed_data['timestamp'])
            s3_key_processed = f"weather_data/processed/{os.path.basename(s3_key_processed)}"
            upload_to_s3(processed_file_path, s3_bucket, s3_key_processed, s3_region)

if __name__ == "__main__":
    main()
