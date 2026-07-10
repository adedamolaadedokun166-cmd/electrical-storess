import html
import os
import re

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request, redirect, session, url_for

from admin_utils import export_subscribers_csv, get_admin_credentials, get_admin_data
from init_db import get_db_connection, init_db

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "ade-ade-electricals")
app.config["FLASK_ENV"] = os.getenv("FLASK_ENV", "development")
app.config["DATABASE_PATH"] = os.getenv("DATABASE_PATH", "database.db")
app.config["SESSION_COOKIE_HTTPONLY"] = True

init_db()


def sanitize_text(value):
    if not value:
        return ""
    return html.escape(re.sub(r"\s+", " ", str(value)).strip())


def sanitize_email(value):
    if not value:
        return ""
    return sanitize_text(value).lower()


def get_products(category="all", limit=None, exclude_id=None):
    conn = get_db_connection()
    query = "SELECT * FROM products"
    params = []

    if category and category != "all":
        query += " WHERE lower(category) = ?"
        params.append(category.lower())

    if exclude_id is not None:
        if "WHERE" in query:
            query += " AND id != ?"
        else:
            query += " WHERE id != ?"
        params.append(exclude_id)

    query += " ORDER BY id DESC"
    if limit is not None:
        query += " LIMIT ?"
        params.append(limit)

    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_product(product_id=None, sku=None):
    conn = get_db_connection()
    if sku:
        row = conn.execute("SELECT * FROM products WHERE lower(sku) = ?", (sku.strip().lower(),)).fetchone()
    elif product_id is not None:
        row = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    else:
        row = None
    conn.close()
    return dict(row) if row else None


@app.route("/")
def index():
    products = get_products(limit=6)
    return render_template("index.html", products=products)


@app.route("/products")
def products():
    category = request.args.get("category", "all")
    products = get_products(category=category)
    return render_template("product-categories.html", products=products, selected_category=category)


@app.route("/product-details")
@app.route("/product-details/<int:product_id>")
def product_details(product_id=None):
    sku = request.args.get("sku", "").strip()
    if product_id is None:
        product_id = request.args.get("product_id", type=int)

    product = get_product(product_id=product_id, sku=sku) if (product_id is not None or sku) else None
    if not product:
        fallback_products = get_products(limit=1)
        product = fallback_products[0] if fallback_products else None

    related_products = []
    if product:
        related_products = get_products(category=product["category"], limit=4, exclude_id=product["id"])

    return render_template("product-details.html", product=product, related_products=related_products)


@app.route("/projects")
def projects():
    return render_template("projects.html")


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        creds = get_admin_credentials()
        if username == creds["username"] and password == creds["password"]:
            session["admin_authenticated"] = True
            return redirect(url_for("admin_dashboard"))
        return render_template("admin/login.html", error="Invalid username or password")

    if session.get("admin_authenticated"):
        return redirect(url_for("admin_dashboard"))
    return render_template("admin/login.html", error=None)


@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin_authenticated"):
        return redirect(url_for("admin_login"))

    messages, subscribers, products = get_admin_data()
    edit_product = request.args.get("edit_id", type=int)
    selected_product = None
    if edit_product:
        conn = get_db_connection()
        row = conn.execute("SELECT * FROM products WHERE id = ?", (edit_product,)).fetchone()
        conn.close()
        selected_product = dict(row) if row else None

    return render_template("admin/dashboard.html", messages=messages, subscribers=subscribers, products=products, edit_product=selected_product)


@app.route("/admin/products", methods=["POST"])
def admin_products():
    if not session.get("admin_authenticated"):
        return redirect(url_for("admin_login"))

    edit_id = request.args.get("edit_id", type=int)
    data = request.form
    name = sanitize_text((data.get("name") or "").strip())
    category = sanitize_text((data.get("category") or "").strip().lower())
    description = sanitize_text((data.get("description") or "").strip())
    sku = sanitize_text((data.get("sku") or "").strip())
    stock_status = sanitize_text((data.get("stock_status") or "In Stock").strip())
    image_url = sanitize_text((data.get("image_url") or "").strip())

    if not all([name, category, description, sku, image_url]):
        return redirect(url_for("admin_dashboard"))

    conn = get_db_connection()
    if edit_id:
        conn.execute(
            "UPDATE products SET name=?, category=?, description=?, sku=?, stock_status=?, image_url=? WHERE id=?",
            (name, category, description, sku, stock_status, image_url, edit_id),
        )
    else:
        conn.execute(
            "INSERT INTO products (name, category, description, sku, stock_status, image_url) VALUES (?, ?, ?, ?, ?, ?)",
            (name, category, description, sku, stock_status, image_url),
        )
    conn.commit()
    conn.close()
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/products/<int:product_id>/delete")
def delete_product(product_id):
    if not session.get("admin_authenticated"):
        return redirect(url_for("admin_login"))

    conn = get_db_connection()
    conn.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/subscribers/export")
def export_subscribers():
    if not session.get("admin_authenticated"):
        return redirect(url_for("admin_login"))
    return export_subscribers_csv()


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_authenticated", None)
    return redirect(url_for("admin_login"))


@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("errors/500.html"), 500


@app.post("/api/contact")
def api_contact():
    data = request.get_json(silent=True)
    if data is None:
        data = request.form
    if not isinstance(data, dict):
        return jsonify({"success": False, "message": "Please fill in all fields with a valid email address."}), 400

    name = sanitize_text((data.get("name") or "").strip())
    phone = sanitize_text((data.get("phone") or "").strip())
    email = sanitize_email((data.get("email") or "").strip())
    subject = sanitize_text((data.get("subject") or "").strip())
    message = sanitize_text((data.get("message") or "").strip())

    if not all([name, phone, email, subject, message]) or "@" not in email:
        return jsonify({"success": False, "message": "Please fill in all fields with a valid email address."}), 400

    try:
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO contacts (name, phone, email, subject, message) VALUES (?, ?, ?, ?, ?)",
            (name, phone, email, subject, message),
        )
        conn.commit()
        conn.close()
    except Exception:
        return jsonify({"success": False, "message": "Unable to save your message right now. Please try again later."}), 500

    return jsonify({"success": True, "message": "Message received. We will contact you shortly."})


@app.post("/api/subscribe")
def api_subscribe():
    data = request.get_json(silent=True)
    if data is None:
        data = request.form
    if not isinstance(data, dict):
        return jsonify({"success": False, "message": "Please enter a valid email address."}), 400

    email = sanitize_email((data.get("email") or "").strip())

    if not email or "@" not in email:
        return jsonify({"success": False, "message": "Please enter a valid email address."}), 400

    try:
        conn = get_db_connection()
        existing = conn.execute("SELECT id FROM subscribers WHERE email = ?", (email,)).fetchone()
        if existing:
            conn.close()
            return jsonify({"success": True, "message": "This email is already subscribed."})

        conn.execute("INSERT INTO subscribers (email) VALUES (?)", (email,))
        conn.commit()
        conn.close()
    except Exception:
        return jsonify({"success": False, "message": "Unable to save your subscription right now. Please try again later."}), 500

    return jsonify({"success": True, "message": "Thank you for subscribing to our updates."})


if __name__ == "__main__":
    app.run(debug=True)
