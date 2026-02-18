"""
NetMonitor UI Styles
Author: Abdullah Ahmed
Year: 2026
"""

class Theme:
    # Colors
    PRIMARY = "#2C3E50"      # Dark Blue - Sidebar/Header
    SECONDARY = "#3498DB"    # Bright Blue - Accents/Buttons
    ACCENT = "#ECF0F1"       # Light Gray - Background
    TEXT_PRIMARY = "#2C3E50" # Dark Text
    TEXT_SECONDARY = "#7F8C8D" # Gray Text
    SUCCESS = "#27AE60"      # Green
    WARNING = "#F39C12"      # Orange
    DANGER = "#C0392B"       # Red
    WHITE = "#FFFFFF"
    
    # Fonts
    FONT_FAMILY = "Segoe UI"
    HEADER_FONT_SIZE = "18px"
    BODY_FONT_SIZE = "14px"
    SMALL_FONT_SIZE = "12px"

    # Stylesheets
    MAIN_WINDOW_STYLE = f"""
        QMainWindow {{
            background-color: {ACCENT};
        }}
    """
    
    SIDEBAR_STYLE = f"""
        QWidget {{
            background-color: {PRIMARY};
            color: {WHITE};
        }}
        QPushButton {{
            background-color: transparent;
            color: {WHITE};
            text-align: left;
            padding: 15px;
            border: none;
            font-size: 16px;
            border-left: 4px solid transparent;
        }}
        QPushButton:hover {{
            background-color: {SECONDARY};
        }}
        QPushButton:checked {{
            background-color: {SECONDARY};
            border-left: 4px solid {WHITE};
            font-weight: bold;
        }}
    """
    
    CARD_STYLE = f"""
        QFrame {{
            background-color: {WHITE};
            border-radius: 8px;
            border: 1px solid #BDC3C7;
        }}
        QLabel {{
            color: {TEXT_PRIMARY};
            border: none;
        }}
    """
    
    TABLE_STYLE = f"""
        QTableWidget {{
            background-color: {WHITE};
            border: 1px solid #BDC3C7;
            gridline-color: #ECF0F1;
            color: {TEXT_PRIMARY};
        }}
        QHeaderView::section {{
            background-color: {PRIMARY};
            color: {WHITE};
            padding: 5px;
            border: none;
        }}
        QTableWidget::item {{
            padding: 5px;
        }}
    """

    BUTTON_STYLE = f"""
        QPushButton {{
            background-color: {SECONDARY};
            color: {WHITE};
            border-radius: 4px;
            padding: 8px 16px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: #2980B9;
        }}
    """