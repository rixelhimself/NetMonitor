"""
NetMonitor
Author: Abdullah Ahmed
Year: 2026
Second-Year Cybersecurity Student Project
All Rights Reserved.

This software is free for academic and personal use.
Commercial usage or redistribution requires explicit permission from the author.
"""

import sys
import os
import threading
import time
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from database.models import DatabaseManager
from gui.main_window import MainWindow
from core.scanner import NetworkScanner
from core.packet_sniffer import PacketSniffer
from core.port_scanner import PortScanner
from core.vulnerability_checker import VulnerabilityChecker
from core.ids_engine import IDSEngine
from reports.report_generator import ReportGenerator

from PyQt6.QtCore import QObject, pyqtSignal

class WorkerSignals(QObject):
    """
    Defines signals for thread communication.
    """
    device_discovered = pyqtSignal(list)
    alert_triggered = pyqtSignal(str, str, str, str) # timestamp, severity, type, description
    stats_updated = pyqtSignal(dict)

class NetMonitorApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.signals = WorkerSignals()
        
        self.db_manager = DatabaseManager()
        self.scanner = NetworkScanner()
        self.sniffer = PacketSniffer()
        self.port_scanner = PortScanner()
        self.vuln_checker = VulnerabilityChecker()
        self.ids = IDSEngine()
        self.reporter = ReportGenerator()
        
        # Initialize Database
        self.db_manager.initialize_tables()
        
        # GUI
        self.main_window = MainWindow()
        
        # Connect Report Button
        self.main_window.reports_page.generate_btn.clicked.connect(self.generate_report)
        
        # Connect Signals
        self.signals.device_discovered.connect(self.update_device_gui)
        self.signals.alert_triggered.connect(self.add_alert_to_gui)
        self.signals.stats_updated.connect(self.update_stats_gui)

        # State
        self.devices = []
        self.alerts = []

        # Timers
        self.scan_timer = QTimer()
        self.scan_timer.timeout.connect(self.run_network_scan)
        self.scan_timer.start(30000) # Scan every 30 seconds

        self.stats_timer = QTimer()
        self.stats_timer.timeout.connect(self.emit_stats)
        self.stats_timer.start(1000) # Update stats every second

    def start(self):
        """
        Starts the application and background threads.
        """
        # Start Sniffer
        self.sniffer.start_sniffing()
        
        # Initial Scan
        threading.Thread(target=self.run_network_scan, daemon=True).start()
        
        self.main_window.show()
        sys.exit(self.app.exec())

    def run_network_scan(self):
        """
        Runs ARP scan and Port scan in background.
        """
        print("Running network scan...")
        found_devices = self.scanner.scan_network()
        
        # Check for new devices and update DB
        # Logic simplified for thread context
        # In a robust app, use a proper diffing strategy
        
        current_macs = {d['mac'] for d in self.devices}
        
        for device in found_devices:
            if device['mac'] not in current_macs:
                # New device logic
                self.ids.check_new_device(device['ip'], device['mac'])
                self.db_manager.add_device(device['ip'], device['mac'])
                
                # Trigger Alert via Signal
                self.signals.alert_triggered.emit(
                    time.strftime("%H:%M:%S"), "Low", "New Device", f"New device joined: {device['ip']}"
                )
                
                # Scan ports for new device
                self.scan_device_ports(device['ip'])
        
        self.devices = found_devices
        # Emit signal to update GUI safely
        self.signals.device_discovered.emit(self.devices)

    def update_device_gui(self, devices):
        """
        Slot to update device view and network map.
        """
        self.main_window.devices_page.update_devices(devices)
        self.main_window.map_page.update_graph(devices)
        
        # Dashboard stats update is handled via update_stats_gui

    def scan_device_ports(self, ip):
        """
        Scans ports and checks vulnerabilities.
        """
        def _scan():
            open_ports = self.port_scanner.scan_device(ip)
            if open_ports:
                self.db_manager.save_scan_result(ip, open_ports)
                vulns = self.vuln_checker.check_vulnerabilities(ip, open_ports)
                for vuln in vulns:
                    # Log to DB through IDs Engine or directly
                    self.ids.trigger_alert(
                        "Vulnerability Detected",
                        f"{vuln['description']} on {vuln['ip']}:{vuln['port']}",
                        vuln['severity']
                    )
                    # Emit signal for GUI
                    self.signals.alert_triggered.emit(
                        time.strftime("%H:%M:%S"),
                        vuln['severity'],
                        "Vulnerability",
                        vuln['description']
                    )
        
        threading.Thread(target=_scan, daemon=True).start()

    def emit_stats(self):
        """
        Calculates stats and emits signal.
        """
        stats = self.sniffer.get_stats()
        new_alerts = self.ids.analyze_traffic(stats)
        
        # Process IDS alerts
        for alert in new_alerts:
            self.signals.alert_triggered.emit(
                time.strftime("%H:%M:%S"),
                alert['severity'],
                alert['type'],
                alert['description']
            )
        
        # Add aggregated stats
        stats['device_count'] = len(self.devices)
        stats['alert_count'] = len(self.alerts)
        
        # Compatibility renames if needed, but Dashboard expects:
        # device_count, pps, upload, download, alert_count
        # PacketSniffer provides: packets_per_second, upload_speed, download_speed
        
        gui_stats = {
            'device_count': len(self.devices),
            'pps': stats.get('packets_per_second', 0),
            'upload': stats.get('upload_speed', 0),
            'download': stats.get('download_speed', 0),
            'alert_count': len(self.alerts)
        }
        
        self.signals.stats_updated.emit(gui_stats)

    def update_stats_gui(self, stats):
        """
        Slot to update stats GUI.
        """
        self.main_window.dashboard_page.update_stats(stats)

    def add_alert_to_gui(self, timestamp, severity, alert_type, description):
        """
        Slot to add alert to GUI.
        """
        self.alerts.append({
            "timestamp": timestamp,
            "severity": severity,
            "type": alert_type,
            "description": description
        })
        self.main_window.alerts_page.add_alert(timestamp, severity, alert_type, description)
        # Dashboard alert count will update on next stats tick

    def generate_report(self):
        """
        Generates PDF report.
        """
        filename = self.reporter.generate_report(self.devices, self.alerts)
        print(f"Report generated: {filename}")


if __name__ == "__main__":
    # Ensure root/admin
    # In Linux, check os.geteuid() == 0
    if hasattr(os, 'geteuid') and os.geteuid() != 0:
        print("WARNING: Not running as root. Sniffing and scanning might fail.")
    
    app = NetMonitorApp()
    app.start()
