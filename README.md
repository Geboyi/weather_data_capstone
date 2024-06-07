# Weather Data Processing Project

## Overview
This project fetches weather data from the Visual Crossing API at regular hourly intervals, processes the data, and stores it in an S3 bucket and locally for further analysis and visualization. The project is structured to facilitate batch processing of weather data and employs GitHub Actions for scheduling and automation. Terraform for AWS S3 resource provisioning. 

## Architecture
Kindly find the architecture of the project via the link below:
- ![Project Architecture](https://drive.google.com/file/d/1pt6APvVT29ZSzdU-FRpImCMJf_vCHKbC/view?usp=sharing)

## Project Scenario
Imagine you are working on a project where you need to continuously monitor and analyze weather data to provide insights and forecasts. This project is designed to automate the collection and processing of weather data, ensuring that you always have the latest information available for analysis.

## Project Structure
```
weather_data_p
├─ .github
│ └─ workflows
│ └─ terraform.yml
├─ .gitignore
├─ config
│ └─ config.json
├─ data
│ ├─ processed
│ └─ raw
├─ README.md
├─ requirements.txt
├─ scripts
│ ├─ fetch.py
│ ├─ pipeline.py
│ └─ process.py
└─ terraform
├─ backend.tf
├─ main.tf
├─ output.tf
└─ variables.tf
```

## Tools and Technologies
- **Python**: For scripting and data processing.
- **Boto3**: For interacting with AWS S3.
- **GitHub Actions**: For scheduling and automation.
- **Terraform**: For infrastructure as code (optional, depending on your deployment strategy).
- **Visual Crossing API**: Source of weather data.
- **AWS S3**: For storing raw and processed data.

## Process and Procedure

### 1. Setup and Configuration
1. Clone the repository to your local machine.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
3. Configure the project by setting your API key and other settings in config/config.yaml.

### 2. Fetching Weather Data
The fetch.py script fetches data from the VisualCrossing API and uploads the raw data to an S3 bucket and saves it locally in the data/raw directory.
##### Run the fetch script
python scripts/fetch.py

### 3. Processing Weather Data
The process.py script processes the raw data and saves the processed data locally in the data/processed directory and uploads it to the S3 bucket.
#### Run the process script
python scripts/process.py

### 4. Running the Pipeline
The pipeline.py script orchestrates the entire pipeline by running the fetch and process scripts.
#### Run the entire pipeline
python scripts/pipeline.py

### 5. Scheduling with GitHub Actions
The project uses GitHub Actions to run the pipeline hourly. The workflow configuration is located in .github/workflows/terraform.yml.

## Importance of the Project
- Automation: Automates the process of fetching and processing weather data.
- Scalability: Easily scalable by leveraging cloud services like AWS S3.
- Reliability: Ensures continuous and timely data availability.
- Integration: Uses modern CI/CD practices with GitHub Actions for automation and scheduling.

## Detailed Steps for Using GitHub Actions
### 1. Setup GitHub Secrets:
- Add your AWS credentials and any other sensitive information as secrets in your GitHub repository.
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
    - S3_BUCKET_NAME
    - AWS_REGION

### 2. GitHub Actions Workflow:
The workflow defined in .github/workflows/terraform.yml will trigger the pipeline to run hourly. Ensure the YAML file is correctly configured with your specific requirements.

## Notes
- Adjust the fetch interval in config/config.yaml as needed.
- Ensure you have the necessary AWS permissions to upload data to S3.




