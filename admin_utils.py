import csv
import os
import sqlite3
from io import StringIO

from flask import Response

from init_db import get_db_connection


def get_admin_credentials():
    return {
        "username": os.getenv("ADMIN_USERNAME", "admin"),
        "password": os.getenv("ADMIN_PASSWORD", "admin123"),
    }


def get_admin_data():
    conn = get_db_connection()
    messages = conn.execute(
        "SELECT id, name, phone, email, subject, message, timestamp FROM contacts ORDER BY id DESC"
    ).fetchall()
    subscribers = conn.execute(
        "SELECT id, email, timestamp FROM subscribers ORDER BY id DESC"
    ).fetchall()
    products = conn.execute(
        "SELECT id, name, category, description, sku, stock_status, image_url FROM products ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return [dict(row) for row in messages], [dict(row) for row in subscribers], [dict(row) for row in products]


def export_subscribers_csv():
    messages, subscribers, _ = get_admin_data()
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=["id", "email", "timestamp"])
    writer.writeheader()
    for row in subscribers:
        writer.writerow(row)
    output.seek(0)
    return Response(output.getvalue(), mimetype="text/csv", headers={"Content-Disposition": "attachment; filename=subscribers.csv"})
