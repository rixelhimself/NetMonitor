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
import struct
from scapy.all import ARP, Ether, srp
import fcntl
import ipaddress
from core.utils import validate_ip

class NetworkScanner:
    """
    Handles automatic subnet detection and ARP scanning for device discovery.
    """
    
    def get_local_ip(self):
        """
        Detects the local IP address of the machine.
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception:
            return "127.0.0.1"

    def get_subnet(self):
        """
        Automatically calculates the local subnet (e.g., 192.168.1.0/24).
        """
        local_ip = self.get_local_ip()
        if not validate_ip(local_ip):
            print(f"Invalid local IP detected: {local_ip}, defaulting to localhost")
            return "127.0.0.1/24"
            
        # Assuming /24 subnet for local LANs as is common in home/small office setups
        # For a more robust solution, we would need to parse network interfaces
        try:
            network = ipaddress.IPv4Network(f"{local_ip}/24", strict=False)
            return str(network)
        except ValueError:
             return "127.0.0.1/24"

    def scan_network(self):
        """
        Performs an ARP scan to discover active devices on the network.
        Returns a list of dictionaries containing IP and MAC addresses.
        """
        subnet = self.get_subnet()
        print(f"Scanning subnet: {subnet}")
        
        # Create ARP request packet
        arp = ARP(pdst=subnet)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether/arp

        try:
            # Send packet and receive response
            result = srp(packet, timeout=2, verbose=0)[0]
            devices = []
            
            for sent, received in result:
                devices.append({
                    "ip": received.psrc,
                    "mac": received.hwsrc
                })
            
            return devices
        except PermissionError:
            print("Error: Permission denied. Please run as sudo/admin.")
            return []
        except Exception as e:
            print(f"Error scanning network: {e}")
            return []
