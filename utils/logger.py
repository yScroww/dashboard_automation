import logging

def setup_logger():
    """
    Configures a basic logger for the application.
    """
    # Create the logger
    logger = logging.getLogger('automation_logger')
    logger.setLevel(logging.INFO) # Set the minimum level for messages

    # Create a handler to send logs to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create a formatter to define the log message format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(console_handler)
    return logger

# Create the logger instance when the module is imported
logger = setup_logger()