import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import json
import os


def setup_logging(log_path='app.log', max_bytes=10*1024*1024, backup_count=5, level=logging.DEBUG):
    logger = logging.getLogger()
    logger.setLevel(level)

    # Ensure log directory exists
    Path(log_path).parent.mkdir(parents=True, exist_ok=True)

    handler = RotatingFileHandler(log_path, maxBytes=max_bytes, backupCount=backup_count)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Optional: also log to console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

def log_skipped_row(row, reason, file_path):
    row['reason'] = reason
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(row, ensure_ascii=False) + '\n')

