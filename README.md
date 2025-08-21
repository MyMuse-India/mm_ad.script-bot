
# MyMuse AI Copywriter (Production-Ready)

Generate high‑converting scripts (Headline / Hook / Body / CTA) from **real MyMuse reviews**.
Includes **email login/signup**, polished **dark UI**, robust scraping + NLP, and optional **OpenAI** integration.

## Quick Start (Windows 11, VS Code)
1. Open folder in VS Code
2. Create venv
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Install deps
   ```bash
   pip install -r requirements.txt
   ```
4. (Optional) set OpenAI key
   ```bash
   set OPENAI_API_KEY=sk-...
   ```
5. Run
   ```bash
   python app.py
   ```
   Visit http://localhost:8000

## Add to GitHub (first time)
Run these in Windows PowerShell from the project root `C:\Users\nihar\Downloads\mymuse_copy_pro`.

1) Initialize git and set your name/email
```powershell
git init
git config user.name "Your Name"
git config user.email "your@email.com"
```

2) Create a .gitignore (already included). Ensure it ignores `/data`, `/instance`, `.env`, caches.

3) First commit
```powershell
git add .
git commit -m "Initial commit: MyMuse AI Copywriter"
```

4) Create an empty repo on GitHub (via web UI), copy its HTTPS URL, e.g.
`https://github.com/<your-username>/mymuse-copy-pro.git`

5) Add remote and push
```powershell
git remote add origin https://github.com/<your-username>/mymuse-copy-pro.git
git branch -M main
git push -u origin main
```

## Update README locally
After changes:
```powershell
git add README.md
git commit -m "docs: update README"
git push
```

## Recommended .gitignore
Create `.gitignore` in the project root with:
```
__pycache__/
*.py[cod]
*$py.class
.venv/
venv/
ENV/
.DS_Store
Thumbs.db
build/
dist/
*.egg-info/
*.log
*.tmp
.env
.env.*
data/*.csv
data/*.json
data/output_*.json
instance/
*.db
.cache/
.ipynb_checkpoints/
node_modules/
chromedriver*
.vscode/
*.code-workspace
.coverage
pytest_cache/
htmlcov/
```

## Usage
- Sign up (email + password), then log in.
- On Dashboard: enter a **MyMuse product URL** or **paste reviews** (one per line).
- Click **Generate**. You’ll see analysis + AI script (if key set).
- Download JSON or Copy the script.

## Env Vars
- SECRET_KEY — Flask session key
- DATABASE_URL — defaults to sqlite:///app.db
- OPENAI_API_KEY — enable generation
