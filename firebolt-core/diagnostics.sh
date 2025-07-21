#!/bin/bash

echo "🔍 Firebolt Core NYC Demo - System Diagnostics"
echo "=============================================="

# Check Docker
echo "📦 Docker Status:"
docker --version
docker info | grep -E "(Memory|CPUs|Operating System)"
echo ""

# Check containers
echo "🐳 Container Status:"
docker ps -a | grep -E "(firebolt|streamlit)" || echo "No Firebolt containers found"
echo ""

# Check Firebolt Core connectivity
echo "🔗 Firebolt Core Connectivity:"
if docker exec firebolt-core fb -C -c "SELECT 'OK' as status" 2>/dev/null; then
    echo "✅ Firebolt Core is responding"
else
    echo "❌ Firebolt Core is not responding"
fi
echo ""

# Check data
echo "📊 Data Status:"
if docker exec firebolt-core fb -C -c "SELECT COUNT(*) as row_count FROM violations" 2>/dev/null; then
    echo "✅ Data is loaded"
else
    echo "❌ No data found in violations table"
fi
echo ""

# Check Python environment
echo "🐍 Python Environment:"
if [ -d ".venv" ]; then
    echo "✅ Virtual environment exists"
    if [ -f ".venv/bin/activate" ]; then
        source .venv/bin/activate
        python --version
        pip show streamlit plotly pandas 2>/dev/null | grep -E "Name|Version" || echo "❌ Required packages not installed"
    fi
else
    echo "❌ Virtual environment not found"
fi
echo ""

# Check ports
echo "🌐 Port Status:"
if command -v lsof &> /dev/null; then
    lsof -i :3473 | grep LISTEN && echo "✅ Port 3473 (Firebolt Core) is open" || echo "❌ Port 3473 not in use"
    lsof -i :8501 | grep LISTEN && echo "✅ Port 8501 (Streamlit) is open" || echo "❌ Port 8501 not in use"
else
    echo "lsof not available - cannot check ports"
fi

echo ""
echo "🎯 Quick Fix Commands:"
echo "- Restart Firebolt Core: ./setup_core.sh"
echo "- Reload data: ./load_production_data.sh"
echo "- Start Streamlit: source .venv/bin/activate && streamlit run app/streamlit_app.py"

