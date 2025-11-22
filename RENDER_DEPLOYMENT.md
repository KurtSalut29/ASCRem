# ASCReM - Render Deployment Guide

## Prerequisites
1. Git repository with your code
2. Render account (free tier available)

## Deployment Steps

### 1. Environment Setup
- Your `.env` file contains default values
- Render will override these with secure production values

### 2. Database Migration
**Important**: Your current MySQL database needs to be migrated to PostgreSQL for Render.

#### Export Current Data:
```bash
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission > data.json
```

#### After Render Deployment:
```bash
python manage.py loaddata data.json
```

### 3. Deploy to Render
1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Render will automatically detect `render.yaml` and configure everything
4. The build script will handle dependencies and static files

### 4. Environment Variables (Auto-configured)
- `SECRET_KEY`: Auto-generated secure key
- `DEBUG`: Set to False for production
- `DATABASE_URL`: Auto-configured PostgreSQL connection
- `ALLOWED_HOSTS`: Set to your Render domain

## Post-Deployment
1. Create superuser: `python manage.py createsuperuser`
2. Load your data: `python manage.py loaddata data.json`
3. Test your application

## Files Created/Modified
- ✅ `requirements.txt` - Updated with production dependencies
- ✅ `settings.py` - Production-ready configuration
- ✅ `.env` - Environment variables template
- ✅ `build.sh` - Render build script
- ✅ `render.yaml` - Render service configuration
- ✅ `.gitignore` - Version control exclusions

Your application is now Render-ready! 🚀