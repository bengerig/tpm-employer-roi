#!/bin/bash

echo "🚀 Starting TPM Employer ROI App v2.0..."
echo ""
echo "Installing/updating dependencies..."
pip install -r requirements.txt --quiet

echo ""
echo "Launching enhanced app with Database, Auth, Analytics & Export..."
echo "📊 App will open at http://localhost:8501"
echo ""
echo "💡 Demo Login: username=demo, password=demo"
echo ""

streamlit run employer_roi_app.py
