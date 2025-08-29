from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, jsonify
import csv, os, json, datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-me-in-production"  # required for flash messages
app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "static", "uploads")
app.config["DATA_DIR"] = os.path.join(app.root_path, "data")

# Ensure data directory exists
os.makedirs(app.config["DATA_DIR"], exist_ok=True)

PROJECTS_JSON = os.path.join(app.config["DATA_DIR"], "projects.json")
MESSAGES_CSV = os.path.join(app.config["DATA_DIR"], "messages.csv")

def load_projects():
    try:
        with open(PROJECTS_JSON, "r", encoding="utf-8") as f:
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
    # If you add a real resume file to static/, update filename here
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
        when = datetime.datetime.now().isoformat(timespec="seconds")

        # Basic validation
        if not name or not email or not message:
            flash("Please fill in your name, email, and message.", "error")
            return redirect(url_for("contact"))

        # Save to CSV (acts like a simple CRM)
        is_new = not os.path.exists(MESSAGES_CSV)
        with open(MESSAGES_CSV, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if is_new:
                writer.writerow(["timestamp", "name", "email", "subject", "message", "ip"])
            writer.writerow([when, name, email, subject, message, request.remote_addr])

        flash("Thanks! Your message was received. I'll get back to you shortly.", "success")
        return redirect(url_for("contact"))
    return render_template("contact.html")

# Serve a simple sitemap
@app.route("/sitemap.txt")
def sitemap_txt():
    return (
        "https://example.com/\n"
        "https://example.com/projects\n"
        "https://example.com/about\n"
        "https://example.com/contact\n"
        "https://example.com/resume\n"
    ), 200, {"Content-Type": "text/plain; charset=utf-8"}

# Health check
@app.route("/healthz")
def healthz():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
