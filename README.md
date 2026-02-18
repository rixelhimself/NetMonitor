# NetMonitor – Advanced Network Security Tool

**Author:** Abdullah Ahmed
**Year:** 2026
**Project:** Second-Year Cybersecurity Student Project
**License:** Free for academic/personal use.

## 📌 Project Overview
NetMonitor is a professional-grade, desktop-based Local Area Network (LAN) monitoring and Intrusion Detection System (IDS). Built with Python and PyQt6, it provides real-time traffic analysis, active device discovery, vulnerability scanning, and automated security reporting. Use this tool to audit your network hygiene and detect suspicious activity.

## 🏗 System Architecture
The application is modularized into distinct components for scalability and maintainability:

- **Core Logic (`core/`)**: Handles all network operations.
    - `scanner.py`: ARP-based device discovery and subnet calculation.
    - `packet_sniffer.py`: Multi-threaded packet capture and bandwidth monitoring (Upload/Download/PPS).
    - `ids_engine.py`: Heuristic analysis engine for detecting anomalies.
    - `port_scanner.py` & `vulnerability_checker.py`: Threaded port scanning and service risk assessment.
- **Database (`database/`)**: Manages PostgreSQL connections and schema for persistent logging of devices and alerts.
- **GUI (`gui/`)**: A modern, academic-themed PyQt6 interface using a sidebar layout and stacked widgets for seamless navigation.
- **Reporting (`reports/`)**: Generates professional PDF security audits using ReportLab.

## 🛡 IDS Logic & Detection Capabilities
NetMonitor's IDS Engine uses behavioral analysis to trigger alerts:

1.  **New Device Detection**: Flags devices that haven't been seen before in the database.
2.  **Traffic Volumetrics**: Detects abnormal spikes in packets-per-second (PPS) indicating potential DoS/flooding.
3.  **SYN Flood Detection**: Monitors excessive SYN packets from a single source IP.
4.  **Port Scan Detection**: Identifies hosts attempting to connect to multiple unique ports in a short timeframe.
5.  **Risky Service Exposure**: alerts on high-risk open ports (e.g., Telnet-23, SMB-445, RDP-3389).

## Installation & Setup

### Prerequisites
- **Python 3.11+**
- **PostgreSQL Database**
- **libpcap** (Linux) or **Npcap** (Windows) for packet capture.

### Ubuntu / Linux Setup
```bash
# 1. Install System Dependencies
sudo apt update
sudo apt install python3-pip postgresql libpcap-dev python3-venv

# 2. Clone Repository & Create Virtual Environment
git clone <repo-url> netmonitor
cd netmonitor
python3 -m venv venv
source venv/bin/activate

# 3. Install Python Dependencies
pip install -r requirements.txt

# 4. Configure Database
# Create a database named 'netmonitor' in PostgreSQL.
# Copy .env.example to .env and update credentials:
cp .env.example .env
nano .env
```

### Windows Setup
1.  **Install Npcap**: Download from [npcap.com](https://npcap.com/) (Check "Install Npcap in WinPcap API-compatible Mode").
2.  **Install PostgreSQL**: Ensure the server is running.
3.  **Install Python Dependencies**:
    ```cmd
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    ```
4.  **Configure .env**: Set your DB credentials.

## ⏯ Usage
**Crucial Note**: Network sniffing and raw socket operations require **Administrator/Root** privileges.

### Linux
```bash
# Must be run with sudo using the virtual environment's python
sudo ./venv/bin/python main.py
```

### Windows
Run **Command Prompt** or **PowerShell** as **Administrator**.
```cmd
venv\Scripts\python main.py
```

## Security Considerations
- **Root Privileges**: The app requires root to bind to network interfaces. Ensure you trust the code before running.
- **Input Validation**: All user inputs (IPs, strings) are sanitized to prevent SQL injection and command injection.
- **Database Safety**: Uses parameterized queries (`psycopg2`) for all database interactions.
- **Local Use Only**: Designed for LAN environments; do not expose the web/database port to the public internet.

---
© 2026 Abdullah Ahmed – All Rights Reserved
