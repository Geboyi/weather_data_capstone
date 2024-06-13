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

def upload_to_s3(file_path, bucket_name, key, region):
    s3_client = boto3.client('s3', region_name=region)
    try:
        s3_client.upload_file(file_path, bucket_name, key)
        print(f"Processed data uploaded to S3 bucket '{bucket_name}' with key '{key}'")
    except Exception as e:
        print(f"Failed to upload processed data to S3: {e}")

def main():
    config = load_config()
    raw_data_dir = 'data/raw'
    processed_data_dir = 'data/processed'
    
    # Ensure the directories exist
    if not os.path.exists(raw_data_dir):
        os.makedirs(raw_data_dir)
    if not os.path.exists(processed_data_dir):
        os.makedirs(processed_data_dir)

    s3_bucket = config['s3']['bucket']
    s3_region = config['s3']['region']
    s3_key_processed_template = config['s3']['key1']
    
    # Process each raw data file
    for filename in os.listdir(raw_data_dir):
        if filename.endswith('.json'):
            raw_file_path = os.path.join(raw_data_dir, filename)
            with open(raw_file_path, 'r') as file:
                raw_data = json.load(file)
                processed_data = process_weather_data(raw_data)
                
                if processed_data:
                    processed_file_path = save_processed_data(processed_data, processed_data_dir)
                    s3_key_processed = s3_key_processed_template.format(timestamp=processed_data['timestamp'])
                    s3_key_processed = f"weather_data/processed/{os.path.basename(s3_key_processed)}"
                    upload_to_s3(processed_file_path, s3_bucket, s3_key_processed, s3_region)

if __name__ == "__main__":
    main()
