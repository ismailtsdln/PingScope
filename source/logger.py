#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os

LOG_DIR = os.path.expanduser("~/.pyping_logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_FILE = os.path.join(LOG_DIR, "pyping.log")

def setup_logger():
    """Sets up the logging configuration."""
    logger = logging.getLogger("PyPing")
    logger.setLevel(logging.INFO)
    
    # File handler
    fh = logging.FileHandler(LOG_FILE)
    fh.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    
    logger.addHandler(fh)
    return logger

logger = setup_logger()
