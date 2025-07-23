#!/bin/bash

echo "🔍 Firebolt Core NYC Demo - Status Check"
echo "========================================"

# Check Docker
echo "📦 Docker Status:"
if command -v docker &> /dev/null; then
    echo "✅ Docker is installed"
    if docker info >/dev/null 2>&1; then
        echo "✅ Docker is running"
    else
        echo "❌ Docker is not running"
        exit 1
    fi
else
    echo "❌ Docker is not installed"
    exit 1
fi

# Check Firebolt Core container
echo ""
echo "🐳 Firebolt Core Status:"
if docker ps | grep -q firebolt-core; then
    echo "✅ Firebolt Core container is running"
    if docker exec firebolt-core fb -C -c "SELECT 1" >/dev/null 2>&1; then
        echo "✅ Firebolt Core is responding to queries"
    else
        echo "❌ Firebolt Core is not responding"
        exit 1
    fi
else
    echo "❌ Firebolt Core container is not running"
    echo "💡 Run: ./setup_core.sh"
    exit 1
fi

# Check data
echo ""
echo "📊 Data Status:"
if docker exec firebolt-core fb -C -c "SELECT COUNT(*) FROM violations" >/dev/null 2>&1; then
    row_count=$(docker exec firebolt-core fb -C -c "SELECT COUNT(*) FROM violations" 2>/dev/null | grep -o "[0-9]*" | head -n1)
    echo "✅ Data is loaded: $row_count rows in violations table"
else
    echo "❌ No data found in violations table"
    echo "💡 Run: ./load_data.sh"
    exit 1
fi

# Check Python environment
echo ""
echo "🐍 Python Environment:"
if [ -d ".venv" ]; then
    echo "✅ Virtual environment exists"
    if source .venv/bin/activate && python -c "import streamlit, plotly, pandas" 2>/dev/null; then
        echo "✅ Required Python packages are installed"
    else
        echo "❌ Required Python packages are missing"
        echo "💡 Run: pip install -r requirements.txt"
        exit 1
    fi
else
    echo "❌ Virtual environment not found"
    echo "💡 Run: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Check if Streamlit is running
echo ""
echo "🌐 Streamlit Status:"
if curl -s http://localhost:8501/_stcore/health >/dev/null 2>&1; then
    echo "✅ Streamlit is running at http://localhost:8501"
else
    echo "❌ Streamlit is not running"
    echo "💡 Run: source .venv/bin/activate && streamlit run app/streamlit_app.py"
fi

echo ""
echo "🎯 Summary:"
echo "✅ System is ready for benchmarking!"
echo "🚀 Open http://localhost:8501 in your browser" 