# Ade & Ade Electricals

A Flask-based electrical and solar products website with dynamic catalog pages, contact and newsletter forms, an admin dashboard, and deployment-ready configuration.

## Run locally

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
python app.py
```

## Production deployment

This project includes deployment files for Render:
- render.yaml
- Procfile
- runtime.txt

### Environment variables
- SECRET_KEY
- FLASK_ENV=production
- DATABASE_PATH=database.db

### Backup database
```bash
python backup_db.py
```
