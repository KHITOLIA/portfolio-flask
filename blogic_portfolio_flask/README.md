# Tushar — Data Science & Gen‑AI Trainer (Flask Portfolio)

A clean, modern portfolio website built with Flask + Tailwind (CDN).

## Features
- Home, Projects, About, Contact, Resume pages
- Projects loaded from `data/projects.json`
- Contact form stores entries in `data/messages.csv`
- Dark mode with localStorage toggle
- Minimal Tailwind styles via CDN (no build step)
- API route `/api/projects` for JSON

## Quickstart
```bash
# 1) Create & activate a virtual environment (Windows PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Run the app
python app.py
# Open http://127.0.0.1:5000
```

## Customization
- Update text in templates under `templates/`
- Add your resume PDF to `static/Tushar_T_Blogic_Resume.pdf`
- Edit projects in `data/projects.json`
- Change email/branding in `templates/base.html`

## Deploy options
- Gunicorn + Nginx (Linux server)
- Render/Heroku/Fly.io
- Docker (optional, simple example below)

### Optional Docker
```dockerfile
# Dockerfile (optional)
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PORT=5000
CMD ["python", "app.py"]
```
```bash
docker build -t tushar-portfolio .
docker run -p 5000:5000 tushar-portfolio
```

---
© 2025 Tushar — All rights reserved.
