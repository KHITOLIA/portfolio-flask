from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, jsonify
import os, json, datetime, psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-me-in-production"  # required for flash messages
app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "static", "uploads")

# Database connection string (Render me env var se set hoga)
DATABASE_URL = os.getenv("DATABASE_URL")

# --- Helper: Get DB Connection ---
def get_db():
    conn = psycopg2.connect(DATABASE_URL, sslmode="require")
    return conn

# --- Create table if not exists ---
def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP,
            name TEXT,
            email TEXT,
            subject TEXT,
            message TEXT,
            ip TEXT
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

init_db()

# --- Dummy projects loader (JSON file optional) ---
def load_projects():
    projects_path = os.path.join(app.root_path, "data", "projects.json")
    try:
        with open(projects_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

@app.route("/")
def home():
    return render_template("index.html", projects=load_projects())

@app.route("/projects")
def projects():
    return render_template("projects.html", projects=load_projects())

@app.route("/api/projects")
def api_projects():
    return jsonify(load_projects())

@app.route("/resume")
def resume():
    resume_filename = "Tushar_T_Blogic_Resume.pdf"
    resume_path = os.path.join(app.root_path, "static", resume_filename)
    if os.path.exists(resume_path):
        return send_from_directory(os.path.join(app.root_path, "static"), resume_filename, as_attachment=True)
    return render_template("resume.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        subject = request.form.get("subject", "").strip()
        message = request.form.get("message", "").strip()
        when = datetime.datetime.now()
        ip = request.remote_addr

        if not name or not email or not message:
            flash("Please fill in your name, email, and message.", "error")
            return redirect(url_for("contact"))

        # Save to PostgreSQL
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO messages (timestamp, name, email, subject, message, ip) VALUES (%s, %s, %s, %s, %s, %s)",
            (when, name, email, subject, message, ip)
        )
        conn.commit()
        cur.close()
        conn.close()

        flash("Thanks! Your message was received. I'll get back to you shortly.", "success")
        return redirect(url_for("contact"))
    return render_template("contact.html")

# Health check
@app.route("/healthz")
def healthz():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
