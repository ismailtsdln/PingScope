#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import concurrent.futures
import platform
from source.utils import get_ping_command, parse_ping_line

def ping_single_host(ip, count=1, timeout=1):
    """Pings a single host and returns success status and average latency."""
    cmd = get_ping_command(ip, count=count, timeout=timeout)
    latencies = []
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, _ = process.communicate(timeout=timeout + 2)
        
        for line in stdout.splitlines():
            lat = parse_ping_line(line)
            if lat is not None:
                latencies.append(lat)
        
        if latencies:
            return {"host": ip, "status": "UP", "avg_ms": sum(latencies)/len(latencies)}
        return {"host": ip, "status": "DOWN", "avg_ms": None}
    except Exception:
        return {"host": ip, "status": "ERROR", "avg_ms": None}

def scan_hosts(hosts, threads=10, count=1, timeout=1):
    """Scans multiple hosts concurrently."""
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        future_to_host = {executor.submit(ping_single_host, host, count, timeout): host for host in hosts}
        for future in concurrent.futures.as_completed(future_to_host):
            results.append(future.result())
    return results

def trace_route(host):
    """Performs a traceroute to the target host."""
    import platform
    current_os = platform.system().lower()
    
    if current_os == "windows":
        cmd = ["tracert", host]
    else:
        cmd = ["traceroute", host]
        
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        return process
    except Exception:
        return None
