import runpod
import logging
import os
from datetime import datetime

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
    
    f = open(log_filename, "a")
    
    # Log with request ID for traceability
    logging.info(f"Processing request {request_id}")
    f.write(f"Processing request {request_id}\n")

    try:

        print(f"Worker Start")
        input = job["input"]
       
        prompt = input.get("prompt")
        seconds = input.get("seconds", 0)
                
        print(f"Received prompt: {prompt}")
        print(f"Sleeping for {seconds} seconds...")
        
        logging.info(f"Request {request_id} completed successfully")
        f.write(f"Request {request_id} completed successfully\n")
        f.close()
        return prompt
    except Exception as e:
        logging.error(f"Request {request_id} failed: {str(e)}")
        f.write(f"Request {request_id} failed: {str(e)}\n")
        f.close()
        raise

if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})
