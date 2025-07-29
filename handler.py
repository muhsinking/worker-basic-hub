import logging
import os
import runpod
import logging.handlers

def setup_logger(log_dir="/runpod-volume/logs", log_level=logging.INFO):
    """
    Configures and returns a logger that writes to both the console and a
    file on a network volume.

    This function should be called once when the worker initializes.
    """
    # Ensure the log directory exists on the network volume
    os.makedirs(log_dir, exist_ok=True)

    # Define the format for log messages. We include a placeholder for 'request_id'
    # which will be added contextually for each job.
    log_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - [Request: %(request_id)s] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Get the root logger
    logger = logging.getLogger("runpod_worker")
    logger.setLevel(log_level)
    
    # --- Console Handler ---
    # This handler sends logs to standard output, which Runpod captures as Endpoint Logs.
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    
    # --- File Handler ---
    # This handler writes logs to a single file on the persistent network volume.
    # Note: This handler does not rotate logs.
    log_file_path = os.path.join(log_dir, "worker.log")
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setFormatter(log_format)

    # Add both handlers to the logger
    # Check if handlers are already added to avoid duplication on hot reloads
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    
    return logger

# --- Global Logger Initialization ---
# Set up the logger when the script is first loaded by the worker.
# We pass a default request_id that will be used for any logs generated
# outside of the handler function.

# Set log level to DEBUG to capture all levels of logs.
logger = setup_logger(log_level=logging.INFO)
logger = logging.LoggerAdapter(logger, {"request_id": "N/A"})

logger.info("Logger initialized. Ready to process jobs.")


def handler(job):
    """
    This is the main handler function for the Runpod serverless worker.
    It processes a single job and demonstrates all logging levels.
    """
    # Extract the request ID from the job payload for traceability.
    request_id = job.get('id', 'unknown')
    
    # Create a new logger adapter for this specific job. This injects the
    # current request_id into all log messages created with this adapter.
    job_logger = logging.LoggerAdapter(logging.getLogger("runpod_worker"), {"request_id": request_id})
    
    job_logger.info(f"Received job. Now demonstrating all log levels.")
    
    try:
        # --- Demonstrate all log levels sequentially ---
        job_logger.debug("This is a debug message. Use this for detailed information for diagnosing problems.")
        job_logger.info("This is an info message. Use this for general information about program execution.")
        job_logger.warning("This is a warning message. Use this to indicate when something unexpected has occurred, but the program should continue.")
        job_logger.error("This is an error message. Use this for serious but recoverable problems.")
        job_logger.critical("This is a critical message. Use this for very serious and potentially unrecoverable issues.")
        # --- End of demonstration ---

        result = "Successfully demonstrated all log levels."
        job_logger.info(f"Job completed successfully.")
        
        return {"output": result}

    except Exception as e:
        # This block will now only be hit by unexpected errors, not by the demonstration.
        job_logger.error(f"Job failed with an unexpected exception.", exc_info=True)
        return {"error": f"An unexpected error occurred: {str(e)}"}


# Start the serverless worker
if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})
