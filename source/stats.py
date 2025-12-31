#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from datetime import datetime
from source.database import get_history

def generate_graph(host=None, limit=20, output="ping_graph.png"):
    """Generates a latency graph for a specific host or general history."""
    rows = get_history(limit)
    if not rows:
        return False
    
    if host:
        rows = [r for r in rows if r[2] == host]
        
    if not rows:
        return False
        
    # Reverse to get chronological order
    rows = rows[::-1]
    
    timestamps = [datetime.strptime(r[1], "%Y-%m-%d %H:%M:%S") for r in rows]
    avg_latencies = [r[8] for r in rows]
    targets = [r[2] for r in rows]
    
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, avg_latencies, marker='o', linestyle='-', color='b', label='Ort. Gecikme (ms)')
    
    plt.title(f"Ping Gecikme Grafiği {'(' + host + ')' if host else ''}")
    plt.xlabel("Zaman")
    plt.ylabel("Gecikme (ms)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    
    plt.savefig(output)
    plt.close()
    return True
