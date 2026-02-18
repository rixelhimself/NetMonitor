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
from gui.styles import Theme

class DeviceView(QWidget):
    """
    Displays a table of discovered devices.
    """
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        # Header
        header = QLabel("Connected Devices")
        header.setStyleSheet(f"font-size: {Theme.HEADER_FONT_SIZE}; font-weight: bold; color: {Theme.PRIMARY};")
        layout.addWidget(header)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["IP Address", "MAC Address", "Device Name", "Status"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setStyleSheet(Theme.TABLE_STYLE)
        
        layout.addWidget(self.table)

    def add_device(self, device):
        """
        Adds or updates a device in the table.
        device: dict with keys 'ip', 'mac'
        """
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(device['ip']))
        self.table.setItem(row, 1, QTableWidgetItem(device['mac']))
        self.table.setItem(row, 2, QTableWidgetItem(device.get('name', 'Unknown')))
        self.table.setItem(row, 3, QTableWidgetItem("Active"))

    def update_devices(self, devices):
        """
        Updates the table with the latest device list.
        """
        self.table.setRowCount(0)
        for device in devices:
            self.add_device(device)