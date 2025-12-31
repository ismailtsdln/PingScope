#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import os
import sys
import threading
import time

# Add parent directory to path to import source modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from source.scanner import ping_single_host
from source.database import get_history
from source.utils import get_ping_command, parse_ping_line
import subprocess

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pyping_secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/history')
def api_history():
    limit = request.args.get('limit', 10, type=int)
    history = get_history(limit)
    formatted_history = []
    for r in history:
        formatted_history.append({
            "id": r[0],
            "timestamp": r[1],
            "host": r[2],
            "sent": r[3],
            "received": r[4],
            "loss": r[5],
            "min": r[6],
            "max": r[7],
            "avg": r[8],
            "jitter": r[9]
        })
    return jsonify(formatted_history)

@socketio.on('start_ping')
def handle_ping(data):
    host = data.get('host')
    count = data.get('count', 4)
    size = data.get('size', 32)
    
    if not host:
        emit('ping_error', {'message': 'Host is required'})
        return

    def run_ping_thread():
        cmd = get_ping_command(host, count=count, size=size)
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for line in process.stdout:
                line = line.strip()
                if not line: continue
                latency = parse_ping_line(line)
                emit('ping_update', {'line': line, 'latency': latency})
                time.sleep(0.1) # Small delay for UI smoothness
            process.wait()
            emit('ping_complete', {'status': 'finished'})
        except Exception as e:
            emit('ping_error', {'message': str(e)})

    threading.Thread(target=run_ping_thread).start()

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)
