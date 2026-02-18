"""
NetMonitor
Author: Abdullah Ahmed
Year: 2026
Second-Year Cybersecurity Student Project
All Rights Reserved.

This software is free for academic and personal use.
Commercial usage or redistribution requires explicit permission from the author.
"""

import ipaddress
import re

def validate_ip(ip: str) -> bool:
    """
    Validates if the given string is a valid IPv4 address.
    """
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ipaddress.AddressValueError:
        return False

def sanitize_input(input_str: str) -> str:
    """
    Sanitizes string input to prevent injection or format issues.
    Allows alphanumeric, spaces, hyphens, and underscores.
    """
    if not isinstance(input_str, str):
        return ""
    return re.sub(r'[^a-zA-Z0-9 \-_.]', '', input_str)

def validate_port(port: int) -> bool:
    """
    Validates if a port is within the valid range (1-65535).
    """
    try:
        port = int(port)
        return 1 <= port <= 65535
    except (ValueError, TypeError):
        return False
