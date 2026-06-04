#!/usr/bin/env bash
set -e
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env || true
streamlit run app/streamlit_app.py
