"""
NetMonitor
Author: Abdullah Ahmed
Year: 2026
Second-Year Cybersecurity Student Project
All Rights Reserved.

This software is free for academic and personal use.
Commercial usage or redistribution requires explicit permission from the author.
"""

from database.models import DatabaseManager

class IDSEngine:
    """
    Intrusion Detection System Engine.
    Analyzes network activity and triggers alerts.
    """
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.PACKET_THRESHOLD = 1000  # Packets per second to trigger alert
        self.SYN_THRESHOLD = 100 # SYN packets from single IP
        self.PORT_SCAN_THRESHOLD = 20 # Unique ports targeted by single IP

    def analyze_traffic(self, stats):
        """
        Analyzes traffic statistics for anomalies.
        Returns a list of generated alerts.
        """
        new_alerts = []
        
        # Check for high packet rate
        if stats['packets_per_second'] > self.PACKET_THRESHOLD:
            new_alerts.append(self.trigger_alert(
                "High Traffic Volume",
                f"Abnormal traffic spike detected: {int(stats['packets_per_second'])} pps",
                "Medium"
            ))

        # Check for SYN Flood
        for ip, count in stats['syn_counts'].items():
            if count > self.SYN_THRESHOLD:
                new_alerts.append(self.trigger_alert(
                    "Potential SYN Flood",
                    f"Excessive SYN packets from {ip} ({count} packets)",
                    "High"
                ))

        # Check for Port Scanning
        if 'port_scan_counts' in stats:
            for ip, count in stats['port_scan_counts'].items():
                if count > self.PORT_SCAN_THRESHOLD:
                    new_alerts.append(self.trigger_alert(
                        "Port Scanning Activity",
                        f"Host {ip} targeted {count} unique ports",
                        "High"
                    ))
        
        return new_alerts

    def check_new_device(self, ip, mac):
        """
        Checks if a device is new to the network.
        """
        # In a real implementation, we would query the DB to see if device exists.
        # Since 'add_device' updates last_seen if exists, we need a way to know if it was inserted.
        # For simplicity, we will assume the caller handles logic or we check DB first.
        # Here we just log an alert if it is considered 'new' by the caller.
        self.trigger_alert(
            "New Device Detected",
            f"New device joined: {ip} ({mac})",
            "Low"
        )

    def trigger_alert(self, alert_type, description, severity):
        """
        Logs an alert to the database and returns it.
        """
        self.db_manager.log_alert(alert_type, description, severity)
        print(f"IDS ALERT [{severity}]: {alert_type} - {description}")
        return {
            "type": alert_type,
            "description": description,
            "severity": severity
        }
