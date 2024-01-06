import logging

log_handlers = {}

def setup_logging(log_file_path):
    if log_file_path not in log_handlers:
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler(log_file_path, mode='a')
        file_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(message)s')
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

        log_handlers[log_file_path] = logger

    return log_handlers[log_file_path]

def log_message(log_file_path, message):
    logger = setup_logging(log_file_path)
    logger.info(message)