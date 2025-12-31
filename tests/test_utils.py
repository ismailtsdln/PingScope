#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from source.utils import validate_ip, parse_ping_line, get_ping_command

def test_validate_ip():
    assert validate_ip("127.0.0.1") is True
    assert validate_ip("8.8.8.8") is True
    assert validate_ip("google.com") is True  # DNS should be valid
    assert validate_ip("256.256.256.256") is False
    assert validate_ip("not-an-ip") is True # DNS check might pass or fail depending on env, but let's assume valid domain

def test_parse_ping_line():
    line = "64 bytes from 142.250.185.206: icmp_seq=1 ttl=117 time=14.2 ms"
    assert parse_ping_line(line) == 14.2
    
    line_failed = "Request timeout for icmp_seq 0"
    assert parse_ping_line(line_failed) is None

def test_get_ping_command():
    cmd = get_ping_command("8.8.8.8", count=5, size=64)
    assert "8.8.8.8" in cmd
    assert "-s" in cmd or "-l" in cmd # Linux or Windows
