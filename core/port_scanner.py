"""
NetMonitor
Author: Abdullah Ahmed
Year: 2026
Second-Year Cybersecurity Student Project
All Rights Reserved.

This software is free for academic and personal use.
Commercial usage or redistribution requires explicit permission from the author.
"""

import socket
import threading
from concurrent.futures import ThreadPoolExecutor
from core.utils import validate_ip

class PortScanner:
    """
    Scans ports on discovered devices to identify open services.
    """
    def __init__(self):
        self.common_ports = range(1, 1025) # Scan 1-1024
        self.timeout = 1.0

    def scan_device(self, ip):
        """
        Scans a single device for open ports using multiple threads.
        Returns a list of open ports.
        """
        if not validate_ip(ip):
            print(f"Skipping port scan for invalid IP: {ip}")
            return []

        open_ports = []
        print(f"Starting port scan on {ip}...")
        
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = {executor.submit(self._check_port, ip, port): port for port in self.common_ports}
            
            for future in futures:
                result = future.result()
                if result:
                    open_ports.append(result)
        
        return sorted(open_ports)

    def _check_port(self, ip, port):
        """
        Checks if a specific port is open.
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(self.timeout)
                if s.connect_ex((ip, port)) == 0:
                    return port
        except Exception:
            pass
        return None
