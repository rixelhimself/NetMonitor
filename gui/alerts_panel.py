"""
NetMonitor
Author: Abdullah Ahmed
Year: 2026
Second-Year Cybersecurity Student Project
All Rights Reserved.

This software is free for academic and personal use.
Commercial usage or redistribution requires explicit permission from the author.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QLabel
from PyQt6.QtGui import QColor
from gui.styles import Theme

class AlertsPanel(QWidget):
    """
    Displays a log of security alerts.
    """
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        # Header
        header = QLabel("Security Alerts")
        header.setStyleSheet(f"font-size: {Theme.HEADER_FONT_SIZE}; font-weight: bold; color: {Theme.DANGER};")
        layout.addWidget(header)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Timestamp", "Severity", "Type", "Description"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setStyleSheet(Theme.TABLE_STYLE)
        
        layout.addWidget(self.table)

    def add_alert(self, timestamp, severity, alert_type, description):
        """
        Adds a new alert row.
        """
        row = self.table.rowCount()
        self.table.insertRow(row)
        
        self.table.setItem(row, 0, QTableWidgetItem(str(timestamp)))
        
        severity_item = QTableWidgetItem(severity)
        # Color coding
        if severity == "High":
            severity_item.setForeground(QColor(Theme.DANGER))
        elif severity == "Medium":
            severity_item.setForeground(QColor(Theme.WARNING))
        else:
            severity_item.setForeground(QColor(Theme.SECONDARY))
            
        self.table.setItem(row, 1, severity_item)
        self.table.setItem(row, 2, QTableWidgetItem(alert_type))
        self.table.setItem(row, 3, QTableWidgetItem(description))