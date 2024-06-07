import json
import boto3
import os

def load_config():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(script_dir, 'config', 'config.json')
    with open(config_path, 'r') as file:
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
    processed_data_dir = 'data/processed'
    s3_bucket = config['s3']['bucket']
    s3_region = config['s3']['region']
    s3_key_processed = config['s3']['key1']
    
    for filename in os.listdir(processed_data_dir):
        if filename.endswith('.json'):
            with open(os.path.join(processed_data_dir, filename), 'r') as file:
                processed_data = json.load(file)
                processed_file_path = os.path.join(processed_data_dir, filename)
                upload_to_s3(processed_file_path, s3_bucket, s3_key_processed.format(timestamp=processed_data['timestamp']), s3_region)

if __name__ == "__main__":
    main()
