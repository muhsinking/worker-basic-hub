import runpod
import logging
import os
from datetime import datetime

# Configure logging to write to network volume
log_dir = "/runpod-volume/logs"
os.makedirs(log_dir, exist_ok=True)

# Create a timestamped log file
log_filename = f"{log_dir}/worker_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

# Set up file logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()  # Also log to console for Runpod logs
    ]
)

def handler(job):
    request_id = job.get('id', 'unknown')
    
    # Log with request ID for traceability
    logging.info(f"Processing request {request_id}")
    
    try:
        print(f"Worker Start")
        input = job["input"]
        
        result = input.get("prompt")
        seconds = input.get("seconds", 0)
        
        
        print(f"Received prompt: {prompt}")
        print(f"Sleeping for {seconds} seconds...")

        
        logging.info(f"Request {request_id} completed successfully")
        return result
    except Exception as e:
        logging.error(f"Request {request_id} failed: {str(e)}")
        raise

if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})
