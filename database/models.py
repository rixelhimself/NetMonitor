"""
NetMonitor
Author: Abdullah Ahmed
Year: 2026
Second-Year Cybersecurity Student Project
All Rights Reserved.

This software is free for academic and personal use.
Commercial usage or redistribution requires explicit permission from the author.
"""

from database.db_connection import DatabaseConnection
from core.utils import validate_ip, sanitize_input

class DatabaseManager:
    """
    Manages database tables and operations.
    """
    def __init__(self):
        self.db = DatabaseConnection()

    def initialize_tables(self):
        """
        Creates necessary tables if they do not exist.
        """
        cursor = self.db.get_cursor()
        if not cursor:
            return

        queries = [
            """
            CREATE TABLE IF NOT EXISTS devices (
                id SERIAL PRIMARY KEY,
                ip_address VARCHAR(15) UNIQUE NOT NULL,
                mac_address VARCHAR(17) UNIQUE NOT NULL,
                first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                device_name VARCHAR(100)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS alerts (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                alert_type VARCHAR(50) NOT NULL,
                description TEXT,
                severity VARCHAR(10) CHECK (severity IN ('Low', 'Medium', 'High'))
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS scan_results (
                id SERIAL PRIMARY KEY,
                device_ip VARCHAR(15) REFERENCES devices(ip_address) ON DELETE CASCADE,
                open_ports TEXT,
                scan_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        ]

        try:
            for query in queries:
                cursor.execute(query)
            print("Tables initialized successfully.")
        except Exception as e:
            print(f"Error initializing tables: {e}")
        finally:
            cursor.close()

    def add_device(self, ip, mac, name="Unknown"):
        """
        Inserts or updates a device in the database.
        """
        if not validate_ip(ip):
            print(f"Invalid IP address for DB insertion: {ip}")
            return

        cursor = self.db.get_cursor()
        if not cursor:
            return

        query = """
        INSERT INTO devices (ip_address, mac_address, device_name, last_seen)
        VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
        ON CONFLICT (ip_address) 
        DO UPDATE SET last_seen = CURRENT_TIMESTAMP, mac_address = EXCLUDED.mac_address;
        """
        try:
            cursor.execute(query, (ip, mac, sanitize_input(name)))
        except Exception as e:
            print(f"Error adding device: {e}")
        finally:
            cursor.close()

    def log_alert(self, alert_type, description, severity):
        """
        Logs a security alert to the database.
        """
        cursor = self.db.get_cursor()
        if not cursor:
            return

        query = """
        INSERT INTO alerts (alert_type, description, severity)
        VALUES (%s, %s, %s);
        """
        try:
            cursor.execute(query, (alert_type, description, severity))
        except Exception as e:
            print(f"Error logging alert: {e}")
        finally:
            cursor.close()

    def save_scan_result(self, ip, open_ports):
        """
        Saves port scan results.
        """
        if not validate_ip(ip):
            return

        cursor = self.db.get_cursor()
        if not cursor:
            return

        query = """
        INSERT INTO scan_results (device_ip, open_ports)
        VALUES (%s, %s);
        """
        try:
            cursor.execute(query, (ip, str(open_ports)))
        except Exception as e:
            print(f"Error saving scan result: {e}")
        finally:
            cursor.close()