"""
NetMonitor
Author: Abdullah Ahmed
Year: 2026
Second-Year Cybersecurity Student Project
All Rights Reserved.

This software is free for academic and personal use.
Commercial usage or redistribution requires explicit permission from the author.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
from collections import Counter

class ReportGenerator:
    """
    Generates a professional PDF report of network activity and security alerts.
    """
    def generate_report(self, devices, alerts):
        """
        Creates a PDF report in the current directory.
        """
        filename = f"NetMonitor_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        # Title
        title_style = ParagraphStyle(
            'Title',
            parent=styles['Heading1'],
            fontSize=24,
            alignment=TA_CENTER,
            spaceAfter=20,
            textColor=colors.HexColor('#2C3E50')
        )
        story.append(Paragraph("NetMonitor Security Audit Report", title_style))
        story.append(Spacer(1, 10))

        # Metadata
        meta_style = ParagraphStyle(
            'Meta',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.gray,
            alignment=TA_CENTER
        )
        story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", meta_style))
        story.append(Paragraph("Author: Abdullah Ahmed | NetMonitor Tool v1.0", meta_style))
        story.append(Spacer(1, 30))

        # Executive Summary
        story.append(Paragraph("1. Executive Summary", styles['Heading2']))
        story.append(Paragraph("This report provides a summary of network activity, discovered devices, and security alerts detected during the monitoring session. The following data highlights potential risks and network hygiene.", styles['Normal']))
        story.append(Spacer(1, 20))

        # Statistics
        total_devices = len(devices)
        total_alerts = len(alerts)
        severity_counts = Counter(a.get('severity', 'Unknown') for a in alerts)
        
        stats_data = [
            ['Metric', 'Count'],
            ['Total Devices Discovered', str(total_devices)],
            ['Total Alerts Triggered', str(total_alerts)],
            ['High Severity Alerts', str(severity_counts.get('High', 0))],
            ['Medium Severity Alerts', str(severity_counts.get('Medium', 0))],
            ['Low Severity Alerts', str(severity_counts.get('Low', 0))]
        ]
        
        stats_table = Table(stats_data, colWidths=[300, 100])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#2C3E50')),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(stats_table)
        story.append(Spacer(1, 30))

        # Devices Section
        story.append(Paragraph("2. Network Inventory", styles['Heading2']))
        if devices:
            device_data = [['IP Address', 'MAC Address', 'Name', 'Status']]
            for d in devices:
                device_data.append([
                    d.get('ip', 'N/A'),
                    d.get('mac', 'N/A'),
                    d.get('name', 'Unknown'),
                    'Active'
                ])
            
            device_table = Table(device_data, colWidths=[120, 120, 150, 80])
            device_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
            ]))
            story.append(device_table)
        else:
            story.append(Paragraph("No devices detected.", styles['Normal']))
        story.append(Spacer(1, 30))

        # Alerts Section
        story.append(Paragraph("3. Security Alerts Analysis", styles['Heading2']))
        if alerts:
            alert_data = [['Timestamp', 'Severity', 'Type', 'Description']]
            for a in alerts:
                # Truncate description
                desc = a.get('description', '')
                if len(desc) > 50:
                    desc = desc[:47] + "..."
                
                alert_data.append([
                    a.get('timestamp', ''),
                    a.get('severity', ''),
                    a.get('type', ''),
                    desc
                ])
            
            alert_table = Table(alert_data, colWidths=[100, 60, 100, 200])
            # Conditional formatting for severity would be nice but simple table for now
            alert_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#C0392B')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('FONTSIZE', (0, 0), (-1, -1), 9)
            ]))
            story.append(alert_table)
        else:
            story.append(Paragraph("No security alerts generated to date.", styles['Normal']))
            
        # Footer
        story.append(Spacer(1, 50))
        footer_style = ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, alignment=TA_CENTER)
        story.append(Paragraph("© 2026 Abdullah Ahmed – All Rights Reserved", footer_style))

        doc.build(story)
        return filename
