"""
NetMonitor
Author: Abdullah Ahmed
Year: 2026
Second-Year Cybersecurity Student Project
All Rights Reserved.

This software is free for academic and personal use.
Commercial usage or redistribution requires explicit permission from the author.
"""

import threading
import time
import psutil
from scapy.all import sniff, TCP, IP
from collections import defaultdict

class PacketSniffer:
    """
    Captures packets in a background thread and monitors traffic statistics.
    """
    def __init__(self, interface=None):
        self.interface = interface
        self.running = False
        self.packet_count = 0
        self.start_time = 0
        self.syn_packets = defaultdict(int)
        self.syn_target_ports = defaultdict(set) # src_ip -> set(dst_ports)
        self.lock = threading.Lock()
        self.last_bytes_sent = 0
        self.last_bytes_recv = 0
        self.last_stats_time = time.time()

    def start_sniffing(self):
        """
        Starts the packet capturing in a daemon thread.
        """
        self.running = True
        self.start_time = time.time()
        self.sniffer_thread = threading.Thread(target=self._sniff_loop, daemon=True)
        self.sniffer_thread.start()
        print("Packet sniffer started.")

    def stop_sniffing(self):
        """
        Stops the packet capturing thread.
        """
        self.running = False
        print("Packet sniffer stopped.")

    def _sniff_loop(self):
        """
        Internal loop to capture packets using Scapy.
        """
        while self.running:
            try:
                # timeout=1 allows checking self.running periodically
                # store=0 avoids memory buildup
                sniff(prn=self._process_packet, store=0, timeout=1)
            except Exception as e:
                print(f"Sniffing error: {e}")
                time.sleep(1)  # Avoid tight loop on error

    def _process_packet(self, packet):
        """
        Callback to process each captured packet.
        """
        if not self.running:
            return

        with self.lock:
            self.packet_count += 1
            
            # Basic IDS check for SYN flood and Port Scanning
            if packet.haslayer(TCP) and packet[TCP].flags == 'S':
                if packet.haslayer(IP):
                    src_ip = packet[IP].src
                    self.syn_packets[src_ip] += 1
                    self.syn_target_ports[src_ip].add(packet[TCP].dport)

    def get_stats(self):
        """
        Returns current traffic statistics.
        """
        with self.lock:
            elapsed_time = time.time() - self.start_time
            pps = self.packet_count / elapsed_time if elapsed_time > 0 else 0
            
            # Bandwidth calculation
            net_io = psutil.net_io_counters()
            bytes_sent = net_io.bytes_sent
            bytes_recv = net_io.bytes_recv
            
            # Calculate speed (difference from last check would be better, but for now specific values)
            # In a real-time loop we should track delta. 
            # Let's simple fix: store previous values.
            
            upload_speed = 0
            download_speed = 0
            
            if hasattr(self, 'last_bytes_sent'):
                time_delta = time.time() - self.last_stats_time
                if time_delta > 0:
                    upload_speed = (bytes_sent - self.last_bytes_sent) / time_delta
                    download_speed = (bytes_recv - self.last_bytes_recv) / time_delta
            
            self.last_bytes_sent = bytes_sent
            self.last_bytes_recv = bytes_recv
            self.last_stats_time = time.time()

            return {
                "packets_captured": self.packet_count,
                "packets_per_second": pps,
                "syn_counts": dict(self.syn_packets),
                "upload_speed": upload_speed,
                "download_speed": download_speed,
                "port_scan_counts": {k: len(v) for k, v in self.syn_target_ports.items()}
            }
