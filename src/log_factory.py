import os
import logging
from .config import configuration

def create_log_file_path():
    log_folder_path = os.path.abspath(configuration.log_folder_path)
    if not os.path.exists(log_folder_path):
        os.makedirs(log_folder_path)
    log_file_path = os.path.join(log_folder_path, "bot.log")
    return log_file_path

def creating_log():

    # Configure the logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    log_file_path = create_log_file_path()
    # Create a file handler and set the level to DEBUG
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Create a console handler and set the level to INFO
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Get the root logger and add the handlers
    logger = logging.getLogger('')
    for h in logger.handlers:
        logger.removeHandler(h)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logging.info("Starting bot...")
    logging.info(f"Log file: {log_file_path}")
