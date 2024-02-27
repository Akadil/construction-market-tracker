## logging

### About
- DEBUG:
    - These messages are typically used for detailed information useful for debugging purposes.
    - Include information such as variable values, function calls, or other details helpful for diagnosing issues during development.
    - Example: "Calculating the average of the input numbers. Input list: [1, 2, 3, 4, 5]"
- INFO:
    - These messages provide information about the general progress of the application.
    - Include high-level information such as startup messages, configuration details, or major application milestones.
    - Example: "Server started successfully on port 8000."
- WARNING:
    - These messages indicate potential issues that are not critical but may require attention.
    - Include warnings about deprecated features, unusual conditions, or recoverable errors.
    - Example: "Resource usage is high. Consider optimizing the code."
- ERROR:
    - These messages indicate errors that caused the application to fail to perform a specific task.
    - Include details about the error, such as the nature of the problem and any relevant error codes or stack traces.
    - Example: "Failed to connect to the database. Error: Connection refused."
- CRITICAL:
    - These messages indicate critical errors that require immediate attention as they may lead to application failure or data loss.
    - Include information about severe failures or security breaches that need to be addressed urgently.
    - Example: "Security breach detected. Access to sensitive data compromised."

### My interpretation

In general I have to set my own way of interpretation of this. How I want to set it, and what I want to be handled on each level. Totally, up to me

- Debug - all small messages
- Info - about the flow of the program
- Warning - all small warnings. Not so important but worth of considering
- Error - all errors
- Critical - don't even know. Protect against potential cyber attacks

### Usage

```python
import logging

def setup_logging():
    # Create a logger
    logger = logging.getLogger(__name__)

    # Set the logging level
    logger.setLevel(logging.DEBUG)

    # Create a file handler and set its level to DEBUG
    file_handler = logging.FileHandler('app.log')
    file_handler.setLevel(logging.DEBUG)

    # Create a console handler and set its level to INFO
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create a formatter and set the format for log messages
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

def main():
    # Set up logging
    logger = setup_logging()

    # Log some messages
    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    logger.critical('This is a critical message')

if __name__ == "__main__":
    main()


```

