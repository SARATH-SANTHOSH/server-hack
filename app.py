"""
Cyber Defense Console - Flask Backend
Admin Login + SOC Dashboard
"""

from flask import Flask, render_template, jsonify, request, redirect, url_for, session
import psutil
import sqlite3
from functools import wraps

app = Flask(__name__)
app.secret_key = "SUPER_SECRET_KEY_123"  # change in real deployment

DB_NAME = "security.db"

# ---------------- ADMIN CREDENTIALS ----------------
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "cyber@123"

# ---------------- DATABASE ----------------
def get_db():
    return sqlite3.connect(DB_NAME)

# ---------------- LOGIN REQUIRED DECORATOR ----------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

# ---------------- LOGIN PAGE ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid Credentials"

    return render_template("login.html", error=error)

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ---------------- DASHBOARD ----------------
@app.route("/")
@login_required
def dashboard():
    return render_template("dashboard.html")

# ---------------- SYSTEM STATUS API ----------------
@app.route("/status")
@login_required
def status():
    data = {
        "cpu": psutil.cpu_percent(),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent,
        "processes": len(psutil.pids())
    }
    return jsonify(data)

# ---------------- ALERTS ----------------
@app.route("/alerts")
@login_required
def alerts():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT time, attack, severity, explanation FROM alerts ORDER BY time DESC")
    data = cur.fetchall()
    db.close()
    return render_template("alerts.html", alerts=data)

# ---------------- LOGS ----------------
@app.route("/logs")
@login_required
def logs():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT time, message FROM logs ORDER BY time DESC LIMIT 200")
    data = cur.fetchall()
    db.close()
    return render_template("logs.html", logs=data)

# ---------------- MAIN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
