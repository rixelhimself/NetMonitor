"""
NetMonitor
Author: Abdullah Ahmed
Year: 2026
Second-Year Cybersecurity Student Project
All Rights Reserved.

This software is free for academic and personal use.
Commercial usage or redistribution requires explicit permission from the author.
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QStackedWidget, QLabel, QFrame)
from PyQt6.QtCore import Qt
from gui.dashboard import Dashboard
from gui.device_view import DeviceView
from gui.network_map import NetworkMap
from gui.alerts_panel import AlertsPanel
from gui.reports_view import ReportsView
from gui.styles import Theme

class MainWindow(QMainWindow):
    """
    Main application window hosting the dashboard and navigation.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NetMonitor – Network Security Tool")
        self.setGeometry(100, 100, 1280, 850)
        self.setStyleSheet(Theme.MAIN_WINDOW_STYLE)
        
        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        self.sidebar = QFrame()
        self.sidebar.setStyleSheet(Theme.SIDEBAR_STYLE)
        self.sidebar.setFixedWidth(250)
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(0, 20, 0, 20)
        sidebar_layout.setSpacing(10)
        
        # App Title in Sidebar
        title_label = QLabel("NetMonitor")
        title_label.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {Theme.WHITE}; padding-left: 20px;")
        sidebar_layout.addWidget(title_label)
        sidebar_layout.addSpacing(20)

        # Navigation Buttons
        self.btn_dashboard = self.create_nav_button("Dashboard")
        self.btn_devices = self.create_nav_button("Devices")
        self.btn_port_scanner = self.create_nav_button("Port Scanner")
        self.btn_alerts = self.create_nav_button("Alerts")
        self.btn_map = self.create_nav_button("Network Map")
        self.btn_reports = self.create_nav_button("Reports")

        sidebar_layout.addWidget(self.btn_dashboard)
        sidebar_layout.addWidget(self.btn_devices)
        sidebar_layout.addWidget(self.btn_port_scanner)
        sidebar_layout.addWidget(self.btn_alerts)
        sidebar_layout.addWidget(self.btn_map)
        sidebar_layout.addWidget(self.btn_reports)
        sidebar_layout.addStretch()
        
        # Footer
        footer = QLabel("© 2026 Abdullah Ahmed")
        footer.setStyleSheet("color: #BDC3C7; padding-left: 20px; font-size: 10px;")
        sidebar_layout.addWidget(footer)

        main_layout.addWidget(self.sidebar)

        # Main Content Area
        content_area = QWidget()
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        self.stacked_widget = QStackedWidget()
        
        # Pages
        self.dashboard_page = Dashboard()
        self.devices_page = DeviceView()
        self.alerts_page = AlertsPanel()
        self.map_page = NetworkMap()
        # For Port Scanner, we'll use placeholder for now
        self.port_scanner_page = QLabel("Port Scanner Interface (Select a device in 'Devices' to scan)")
        self.port_scanner_page.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.reports_page = ReportsView()

        self.stacked_widget.addWidget(self.dashboard_page)      # Index 0
        self.stacked_widget.addWidget(self.devices_page)        # Index 1
        self.stacked_widget.addWidget(self.port_scanner_page)   # Index 2
        self.stacked_widget.addWidget(self.alerts_page)         # Index 3
        self.stacked_widget.addWidget(self.map_page)            # Index 4
        self.stacked_widget.addWidget(self.reports_page)        # Index 5

        content_layout.addWidget(self.stacked_widget)
        main_layout.addWidget(content_area)

        # Connect Navigation
        self.btn_dashboard.clicked.connect(lambda: self.switch_page(0, self.btn_dashboard))
        self.btn_devices.clicked.connect(lambda: self.switch_page(1, self.btn_devices))
        self.btn_port_scanner.clicked.connect(lambda: self.switch_page(2, self.btn_port_scanner))
        self.btn_alerts.clicked.connect(lambda: self.switch_page(3, self.btn_alerts))
        self.btn_map.clicked.connect(lambda: self.switch_page(4, self.btn_map))
        self.btn_reports.clicked.connect(lambda: self.switch_page(5, self.btn_reports))
        
        # Set default
        self.btn_dashboard.setChecked(True)

    def create_nav_button(self, text):
        btn = QPushButton(text)
        btn.setCheckable(True)
        btn.setAutoExclusive(True)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        return btn

    def switch_page(self, index, button):
        self.stacked_widget.setCurrentIndex(index)
        button.setChecked(True)