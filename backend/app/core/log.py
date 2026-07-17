import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

abs_path_lib_logs = Path(__file__).resolve().parent.parent / "logs"
abs_path_lib_logs.mkdir(parents=True, exist_ok=True)

def get_logger(name: str) -> logging.Logger:
    """Return logger with given name"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = TimedRotatingFileHandler(
            filename=abs_path_lib_logs.joinpath("log.log"),
            interval=1,
            when="midnight",
            backupCount=10,
            encoding='utf-8'
        )
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    return logger
