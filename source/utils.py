#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import platform
import re
import ipaddress

def clear_screen():
    """Clears the terminal screen based on the operating system."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_ping_command(ip, count=None, size=32, timeout=2, continuous=False):
    """Generates the appropriate ping command based on the OS."""
    current_os = platform.system().lower()
    cmd = ["ping"]
    if current_os == "windows":
        if continuous: cmd.append("-t")
        elif count: cmd.extend(["-n", str(count)])
        cmd.extend(["-l", str(size), "-w", str(timeout * 1000)])
    else:
        if not continuous and count: cmd.extend(["-c", str(count)])
        cmd.extend(["-s", str(size), "-W", str(timeout)])
    cmd.append(ip)
    return cmd

def parse_ping_line(line):
    """Parses a single line of ping output to find latency."""
    match = re.search(r'(?:time|süre|time=)\s*([\d.]+)\s*ms', line, re.IGNORECASE)
    if match: return float(match.group(1))
    return None

def validate_ip(ip):
    """Validates if the input is a valid IP or domain."""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        # Check if it's a domain
        domain_regex = r'^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$'
        return re.match(domain_regex, ip, re.IGNORECASE) is not None

def get_subnet_hosts(subnet):
    """Returns a list of hosts in a subnet."""
    try:
        network = ipaddress.ip_network(subnet, strict=False)
        return [str(host) for host in network.hosts()]
    except ValueError:
        return []
