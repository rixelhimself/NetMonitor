from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt
from gui.styles import Theme

class ReportsView(QWidget):
    """
    Interface for generating reports.
    """
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setSpacing(20)

        # Header
        header = QLabel("Report Generation")
        header.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {Theme.PRIMARY};")
        self.layout.addWidget(header)
        
        # Description
        desc = QLabel("Generate a comprehensive PDF report including:\n- Executive Summary\n- Device List\n- Security Alerts\n- Network Topology")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setStyleSheet(f"font-size: 16px; color: {Theme.TEXT_SECONDARY};")
        self.layout.addWidget(desc)

        # Generate Button
        self.generate_btn = QPushButton("Generate PDF Report")
        self.generate_btn.setFixedSize(200, 50)
        self.generate_btn.setStyleSheet(Theme.BUTTON_STYLE)
        self.generate_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.layout.addWidget(self.generate_btn)