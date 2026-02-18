"""
NetMonitor
Author: Abdullah Ahmed
Year: 2026
Second-Year Cybersecurity Student Project
All Rights Reserved.

This software is free for academic and personal use.
Commercial usage or redistribution requires explicit permission from the author.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import networkx as nx
from gui.styles import Theme

class NetworkMap(QWidget):
    """
    Visualizes the network topology using NetworkX and Matplotlib.
    """
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.figure = plt.figure(figsize=(5, 4))
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)
        self.graph = nx.Graph()

    def update_graph(self, devices):
        """
        Updates the network graph with discovered devices.
        """
        self.figure.clear()
        self.graph.clear()
        
        # Add central router node
        router = "Router/Gateway"
        self.graph.add_node(router)
        
        # Add device nodes
        colors = [Theme.SECONDARY] # Router color
        sizes = [1000] # Router size
        
        for device in devices:
            ip = device.get('ip', 'Unknown')
            self.graph.add_node(ip)
            self.graph.add_edge(router, ip)
            colors.append(Theme.ACCENT if device.get('status') != 'Suspicious' else Theme.DANGER)
            sizes.append(600)
        
        # Draw graph
        pos = nx.spring_layout(self.graph, k=0.5, iterations=50)
        ax = self.figure.add_subplot(111)
        ax.set_title("Network Topology", fontsize=10, color='#2C3E50')
        
        nx.draw(
            self.graph, pos, 
            with_labels=True, 
            node_color=colors, 
            node_size=sizes, 
            font_size=8,
            font_color='#2C3E50',
            edge_color='#BDC3C7',
            width=1.5,
            ax=ax
        )
        self.canvas.draw()