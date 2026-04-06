import logging
import os

def setup_logger():
    log_folder = os.path.join(os.getcwd(), "logs")
    os.makedirs(log_folder, exist_ok=True)
    log_file = os.path.join(log_folder, "trading_bot.log")

    logger = logging.getLogger("trading_bot")
    logger.setLevel(logging.INFO)

    if not logger.handlers:  
        file_handler = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger  

logger =setup_logger() 

