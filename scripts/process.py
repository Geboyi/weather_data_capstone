import json
import boto3
import os

def load_config():
    with open('./config/config.json', 'r') as file:
        config = json.load(file)
    return config

def process_weather_data(raw_data):
    processed_data = {
        'temperature': raw_data['main']['temp'],
        'humidity': raw_data['main']['humidity'],
        'weather': raw_data['weather'][0]['description'],
        'timestamp': raw_data['dt']
    }
    return processed_data

def save_processed_data(processed_data, output_dir='data/processed'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    filename = f"{output_dir}/weather_{processed_data['timestamp']}.json"
    with open(filename, 'w') as file:
        json.dump(processed_data, file)
    print(f"Processed data saved locally to {filename}")
    return filename

def download_from_s3(bucket_name, key, download_path, region):
    s3_client = boto3.client('s3', region_name=region)
    try:
        s3_client.download_file(bucket_name, key, download_path)
        print(f"Raw data downloaded from S3 bucket '{bucket_name}' with key '{key}' to {download_path}")
        with open(download_path, 'r') as file:
            raw_data = json.load(file)
        return raw_data
    except Exception as e:
        print(f"Failed to download raw data from S3: {e}")
        return None

def upload_to_s3(file_path, bucket_name, key, region):
    s3_client = boto3.client('s3', region_name=region)
    try:
        s3_client.upload_file(file_path, bucket_name, key)
        print(f"Processed data uploaded to S3 bucket '{bucket_name}' with key '{key}'")
    except Exception as e:
        print(f"Failed to upload processed data to S3: {e}")

def main():
    config = load_config()
    s3_bucket = config['s3']['bucket']
    s3_region = config['s3']['region']
    s3_key_raw = config['s3']['key']
    s3_key_processed_template = config['s3']['key1']
    
    raw_data_dir = 'data/raw'
    processed_data_dir = 'data/processed'
    
    # Ensure the directories exist
    if not os.path.exists(raw_data_dir):
        os.makedirs(raw_data_dir)
    if not os.path.exists(processed_data_dir):
        os.makedirs(processed_data_dir)

    raw_data_file = f"{raw_data_dir}/latest_weather.json"
    raw_data = download_from_s3(s3_bucket, s3_key_raw, raw_data_file, s3_region)
    
    if raw_data:
        processed_data = process_weather_data(raw_data)
        processed_file_path = save_processed_data(processed_data, processed_data_dir)
        s3_key_processed = s3_key_processed_template.format(timestamp=processed_data['timestamp'])
        upload_to_s3(processed_file_path, s3_bucket, s3_key_processed, s3_region)

if __name__ == "__main__":
    main()
