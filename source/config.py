#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml
import os
import json

CONFIG_PATH = "config.yaml"

DEFAULT_CONFIG = {
    "ping": {
        "count": 4,
        "size": 32,
        "timeout": 2,
        "interval": 1
    },
    "scanner": {
        "threads": 10,
        "timeout": 1
    },
    "history": {
        "enabled": True,
        "limit": 50
    },
    "logging": {
        "level": "INFO",
        "path": "~/.pyping_logs/pyping.log"
    }
}

def load_config():
    """Loads configuration from YAML or JSON file."""
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, 'r') as f:
                if CONFIG_PATH.endswith('.yaml') or CONFIG_PATH.endswith('.yml'):
                    return yaml.safe_load(f)
                elif CONFIG_PATH.endswith('.json'):
                    return json.load(f)
        except Exception as e:
            print(f"[!] Config load error: {e}")
    return DEFAULT_CONFIG

config = load_config()
