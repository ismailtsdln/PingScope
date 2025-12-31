#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.expanduser("~/.pyping_history.db")

def init_db():
    """Initializes the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            host TEXT,
            sent INTEGER,
            received INTEGER,
            packet_loss REAL,
            min_ms REAL,
            max_ms REAL,
            avg_ms REAL,
            jitter_ms REAL
        )
    ''')
    conn.commit()
    conn.close()

def save_history(stats):
    """Saves a ping test result to the database."""
    if not stats: return
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO history (timestamp, host, sent, received, packet_loss, min_ms, max_ms, avg_ms, jitter_ms)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        stats['timestamp'],
        stats['host'],
        stats['sent'],
        stats['received'],
        stats['packet_loss_pct'],
        stats['min_ms'],
        stats['max_ms'],
        stats['avg_ms'],
        stats['jitter_ms']
    ))
    conn.commit()
    conn.close()

def get_history(limit=10):
    """Retrieves the last N records from history."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM history ORDER BY id DESC LIMIT ?', (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows
