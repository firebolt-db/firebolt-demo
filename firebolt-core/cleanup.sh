#!/bin/bash

echo "🧹 Cleaning up Firebolt Core NYC Demo"
echo "====================================="

echo "🛑 Stopping Firebolt Core container..."
docker stop firebolt-core 2>/dev/null || true

echo "🗑️  Removing Firebolt Core container..."
docker rm firebolt-core 2>/dev/null || true

echo "🧹 Cleaning up Docker volumes..."
docker volume prune -f >/dev/null 2>&1 || true

echo "📂 Removing persistent data..."
rm -rf firebolt-core-data/

echo "🐍 Removing Python virtual environment..."
rm -rf .venv/

echo "📊 Removing data directory..."
rm -rf data/

echo "✅ Cleanup completed!"
echo ""
echo "🚀 To start fresh, run:"
echo "   ./setup_core.sh"
echo "   python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
echo "   ./load_data.sh"
echo "   streamlit run app/streamlit_app.py" 