"""
NetMonitor
Author: Abdullah Ahmed
Year: 2026
Second-Year Cybersecurity Student Project
All Rights Reserved.

This software is free for academic and personal use.
Commercial usage or redistribution requires explicit permission from the author.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QFrame
from PyQt6.QtCore import Qt
from gui.styles import Theme

class Dashboard(QWidget):
    """
    Main dashboard view aggregating network stats.
    """
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)

        # Header
        header = QLabel("Dashboard Overview")
        header.setStyleSheet(f"font-size: {Theme.HEADER_FONT_SIZE}; font-weight: bold; color: {Theme.PRIMARY};")
        self.layout.addWidget(header)

        # Metrics Grid
        self.metrics_layout = QGridLayout()
        self.metrics_layout.setSpacing(20)
        
        self.card_active = self.create_metric_card("Active Devices", "0")
        self.card_pps = self.create_metric_card("Packets/sec", "0")
        self.card_upload = self.create_metric_card("Upload Speed", "0 KB/s")
        self.card_download = self.create_metric_card("Download Speed", "0 KB/s")
        self.card_alerts = self.create_metric_card("Recent Alerts", "0")
        
        self.metrics_layout.addWidget(self.card_active, 0, 0)
        self.metrics_layout.addWidget(self.card_pps, 0, 1)
        self.metrics_layout.addWidget(self.card_upload, 0, 2)
        self.metrics_layout.addWidget(self.card_download, 1, 0)
        self.metrics_layout.addWidget(self.card_alerts, 1, 1)
        
        self.layout.addLayout(self.metrics_layout)
        self.layout.addStretch()

    def create_metric_card(self, title, value):
        """
        Helper to create a unified metric card widget.
        """
        card = QFrame()
        card.setStyleSheet(Theme.CARD_STYLE)
        card.setFixedSize(200, 120)
        
        layout = QVBoxLayout(card)
        
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet(f"font-size: 14px; color: {Theme.TEXT_SECONDARY};")
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        value_lbl = QLabel(value)
        value_lbl.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {Theme.PRIMARY};")
        value_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addStretch()
        layout.addWidget(title_lbl)
        layout.addWidget(value_lbl)
        layout.addStretch()
        
        return card

    def update_card_value(self, card, value):
        # The card layout has title at index 1, value at index 2 (due to stretch at 0)
        # Actually better to store references, but for now:
        card.layout().itemAt(2).widget().setText(str(value))

    def update_stats(self, stats):
        """
        Updates the top-level metrics.
        Expects stats dict from main.py
        """
        # stats: { 'device_count': int, 'pps': float, 'upload': float, 'download': float, 'alert_count': int }
        device_count = stats.get('device_count', 0)
        pps = stats.get('pps', 0)
        upload = stats.get('upload', 0) / 1024 # KB/s
        download = stats.get('download', 0) / 1024 # KB/s
        alert_count = stats.get('alert_count', 0)

        self.update_card_value(self.card_active, device_count)
        self.update_card_value(self.card_pps, int(pps))
        self.update_card_value(self.card_upload, f"{upload:.1f} KB/s")
        self.update_card_value(self.card_download, f"{download:.1f} KB/s")
        self.update_card_value(self.card_alerts, alert_count)