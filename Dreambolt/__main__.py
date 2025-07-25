"""
Entry point for running DreamBolt as a module.
Enables: python -m cli <command>

Falls back to argparse CLI if typer dependencies fail.
"""

# Try to import the rich CLI, fall back to argparse CLI if dependencies missing
try:
    from cli import app
    app()
except ImportError as e:
    # Fall back to argparse-based CLI
    print(f"ℹ️  Falling back to simplified CLI (missing dependency: {e.name})")
    print("ℹ️  For full rich interface, install: pip install typer rich loguru")
    print()
    
    # Import and run the working CLI
    from cli_working import main as working_main
    working_main() 