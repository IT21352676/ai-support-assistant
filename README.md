﻿# AI Support Assistant

# Create and activate a virtual environment (recommended):

python -m venv venv
source venv/bin/activate # or venv\Scripts\activate on Windows

# Install dependencies:

pip install -r requirements.txt

# Embed and store (data) docs

python run_embedding.py

# Run main

uvicorn app.main:app --reload
