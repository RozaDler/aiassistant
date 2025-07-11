import logging

# create a setup logger function

def setup_logger(name="AiAssistant"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG) # wanna see all log from debug level and above like info warning and more

    #stream handler will print logs to console
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # format for logs
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] --- [%(message)s] ")
    ch.setFormatter(formatter)

    # to prevent duplicate log handlers being added to same logger instance
    if not logger.hasHandlers():
        logger.addHandler(ch)
    
    return logger

logger = setup_logger()

logger.info("Testing logger")