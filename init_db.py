import os
import sqlite3
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

DB_PATH = Path(__file__).resolve().parent / os.getenv("DATABASE_PATH", "database.db")


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS subscribers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            sku TEXT NOT NULL UNIQUE,
            stock_status TEXT NOT NULL,
            image_url TEXT NOT NULL
        )
        """
    )

    product_count = conn.execute("SELECT COUNT(*) AS count FROM products").fetchone()["count"]
    if product_count == 0:
        conn.executemany(
            """
            INSERT INTO products (name, category, description, sku, stock_status, image_url)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    "Premium Switch Panel",
                    "electrical",
                    "Durable switch panel for homes and commercial buildings.",
                    "AAE-1001",
                    "In Stock",
                    "images/tester.jpg",
                ),
                (
                    "Solar Battery Pack",
                    "solar",
                    "Reliable energy storage for uninterrupted solar performance.",
                    "AAE-1002",
                    "In Stock",
                    "images/hammer.jpg",
                ),
                (
                    "Professional Tool Kit",
                    "tools",
                    "High-grade installation tools for electrical professionals.",
                    "AAE-1003",
                    "Limited Stock",
                    "images/plier.jpg",
                ),
                (
                    "Industrial Safety Kit",
                    "safety",
                    "Protective gear for secure and compliant installations.",
                    "AAE-1004",
                    "In Stock",
                    "images/boots.jpg",
                ),
                (
                    "LED Lighting Bundle",
                    "lighting",
                    "Energy-efficient lighting for modern interiors and exteriors.",
                    "AAE-1005",
                    "In Stock",
                    "images/belt.jpg",
                ),
            ],
        )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("Database initialized at", DB_PATH)
