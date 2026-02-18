"""
NetMonitor
Author: Abdullah Ahmed
Year: 2026
Second-Year Cybersecurity Student Project
All Rights Reserved.

This software is free for academic and personal use.
Commercial usage or redistribution requires explicit permission from the author.
"""

import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DatabaseConnection:
    """
    Singleton class to handle PostgreSQL database connections.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.connection = None
        return cls._instance

    def connect(self):
        """
        Establishes a connection to the PostgreSQL database using credentials from .env.
        """
        if self.connection is not None and not self.connection.closed:
            return self.connection

        try:
            self.connection = psycopg2.connect(
                dbname=os.getenv("DB_NAME", "netmonitor"),
                user=os.getenv("DB_USER", "postgres"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST", "localhost"),
                port=os.getenv("DB_PORT", "5432")
            )
            self.connection.autocommit = True
            print("Database connected successfully.")
            return self.connection
        except psycopg2.Error as e:
            print(f"Error connecting to database: {e}")
            return None

    def get_cursor(self):
        """
        Returns a cursor object for executing queries.
        """
        if self.connection is None or self.connection.closed:
            self.connect()
        
        if self.connection:
            return self.connection.cursor()
        return None

    def close(self):
        """
        Closes the database connection.
        """
        if self.connection:
            self.connection.close()
            print("Database connection closed.")