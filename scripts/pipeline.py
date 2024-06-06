import schedule
import time
import subprocess

def run_pipeline():
    subprocess.call(['python', 'scripts/fetch.py'])
    subprocess.call(['python', 'scripts/process.py'])

# Schedule the pipeline to run every hour
schedule.every().hour.do(run_pipeline)

# Run the scheduler continuously
while True:
    schedule.run_pending()
    time.sleep(1)
