"""
DreamBolt CLI - Main entry point for data ingestion and processing.
Typer-based CLI with rich help system and validation.

Enhanced with Firebolt Core support - free, self-hosted analytics.
"""
import typer
from typing import Optional
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from loguru import logger
import sys

from ingest_simple import DataIngester
from synth_simple import DataSynthesizer
from firebolt_io_simple import FireboltConnector, setup_firebolt_core

# Initialize CLI app and console
app = typer.Typer(
    name="dreambolt",
    help="🚀 DreamBolt: AI-powered data ingestion and synthesis pipeline with Firebolt Core",
    rich_markup_mode="rich"
)
console = Console()

# Configure logging
logger.remove()
logger.add(sys.stderr, level="INFO", format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | {message}")


@app.command("ingest")
def ingest_data(
    input_path: str = typer.Argument(
        ..., 
        help="Input data path (CSV/Parquet file or S3 URI)",
        metavar="PATH"
    ),
    output: Optional[str] = typer.Option(
        None,
        "--output", "-o",
        help="Output Parquet file path (default: auto-generated)"
    ),
    table_name: Optional[str] = typer.Option(
        None,
        "--table", "-t",
        help="Firebolt table name (default: derived from filename)"
    ),
    no_synth: bool = typer.Option(
        False,
        "--no-synth",
        help="Skip LLM synthesis step"
    ),
    synthesize: Optional[int] = typer.Option(
        None,
        "--synthesize", "-s",
        help="Number of synthetic rows to generate",
        min=1
    ),
    model: str = typer.Option(
        "openai:gpt-3.5-turbo",
        "--model", "-m",
        help="LLM model for synthesis (e.g., 'openai:gpt-4', 'mistralai/Mistral-7B')"
    ),
    embedding_model: Optional[str] = typer.Option(
        None,
        "--embed",
        help="Generate embeddings using specified model"
    ),
    firebolt_engine: Optional[str] = typer.Option(
        None,
        "--engine",
        help="Firebolt engine name"
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Show what would be done without executing"
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose", "-v",
        help="Enable verbose logging"
    )
):
    """
    🎯 Ingest data from CSV/Parquet and optionally synthesize with LLM.
    
    [bold green]Examples:[/bold green]
    
    Basic ingestion:
    [dim]$ dreambolt ingest data.csv --no-synth[/dim]
    
    With synthesis:
    [dim]$ dreambolt ingest data.csv --synthesize 100 --model openai:gpt-4[/dim]
    
    S3 source:
    [dim]$ dreambolt ingest s3://bucket/data.parquet --table my_table[/dim]
    """
    
    # Configure logging level
    if verbose:
        logger.remove()
        logger.add(sys.stderr, level="DEBUG", format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | {message}")
    
    logger.info(f"🚀 Starting DreamBolt ingestion: {input_path}")
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            
            # Step 1: Data Ingestion
            task1 = progress.add_task("Loading and analyzing data...", total=None)
            ingester = DataIngester()
            df, schema_info = ingester.load_data(input_path)
            logger.info(f"📊 Loaded {len(df)} rows, {len(df.columns)} columns")
            progress.update(task1, completed=True)
            
            # Step 2: Schema Cleaning (always performed)
            task2 = progress.add_task("Cleaning schema...", total=None)
            cleaned_df = ingester.clean_schema(df, schema_info)
            logger.info("🧹 Schema cleaned and validated")
            progress.update(task2, completed=True)
            
            # Step 3: Optional Synthesis
            final_df = cleaned_df
            if not no_synth and synthesize:
                task3 = progress.add_task(f"Synthesizing {synthesize} rows with {model}...", total=None)
                synthesizer = DataSynthesizer(model=model)
                final_df = synthesizer.synthesize_rows(cleaned_df, count=synthesize)
                logger.info(f"🤖 Generated {synthesize} synthetic rows")
                progress.update(task3, completed=True)
            
            # Step 4: Optional Embeddings
            if embedding_model:
                task4 = progress.add_task(f"Generating embeddings with {embedding_model}...", total=None)
                synthesizer = DataSynthesizer(model=embedding_model)
                final_df = synthesizer.add_embeddings(final_df, embedding_model)
                logger.info("🔢 Added embedding columns")
                progress.update(task4, completed=True)
            
            # Step 5: Output Processing
            task5 = progress.add_task("Writing output files...", total=None)
            output_path = output or _generate_output_path(input_path)
            final_df.to_parquet(output_path)
            logger.info(f"💾 Saved to: {output_path}")
            progress.update(task5, completed=True)
            
            # Step 6: Firebolt Integration
            if not dry_run:
                task6 = progress.add_task("Loading to Firebolt...", total=None)
                firebolt = FireboltConnector(engine=firebolt_engine)
                table_name = table_name or _derive_table_name(input_path)
                firebolt.ensure_table(table_name, final_df)
                firebolt.copy_data(table_name, output_path)
                logger.info(f"🔥 Data loaded to Firebolt table: {table_name}")
                progress.update(task6, completed=True)
            else:
                logger.info("🔍 Dry run - skipping Firebolt operations")
        
        console.print("✅ [bold green]Ingestion completed successfully![/bold green]")
        
    except Exception as e:
        logger.error(f"❌ Pipeline failed: {str(e)}")
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise typer.Exit(1)


@app.command("status")
def check_status():
    """🔍 Check DreamBolt and dependency status."""
    console.print("🚀 [bold]DreamBolt Status Check[/bold]")
    
    # Create status table
    table = Table(title="Component Status")
    table.add_column("Component", style="cyan", no_wrap=True)
    table.add_column("Status", style="magenta")
    table.add_column("Version/Info", style="green")
    
    # Check dependencies
    try:
        import pandas
        table.add_row("Pandas", "✅ Available", pandas.__version__)
    except ImportError:
        table.add_row("Pandas", "❌ Not installed", "-")
    
    try:
        from synth_simple import DataSynthesizer
        table.add_row("DataDreamer", "✅ Available", "Fallback mode")
    except ImportError:
        table.add_row("DataDreamer", "❌ Not installed", "-")
    
    # Check Firebolt backends
    try:
        from firebolt_io_simple import FireboltConnector, DOCKER_AVAILABLE
        connector = FireboltConnector()
        
        if connector.backend == "core":
            status = connector.core_status()
            if status.get("status") == "running":
                table.add_row("Firebolt Core", "✅ Running", f"Container: {status.get('container_id', 'N/A')[:12]}")
            elif status.get("status") == "not_created":
                table.add_row("Firebolt Core", "⚪ Not setup", "Run: dreambolt firebolt setup")
            else:
                table.add_row("Firebolt Core", "⚠️ Available", f"Status: {status.get('status', 'unknown')}")
        
        elif connector.backend == "managed":
            table.add_row("Firebolt Managed", "✅ Configured", f"Account: {connector.config.account_name}")
        
        else:
            table.add_row("Firebolt", "🎭 Simulation", "No configuration found")
        
        # Docker status
        if DOCKER_AVAILABLE:
            table.add_row("Docker", "✅ Available", "SDK ready")
        else:
            table.add_row("Docker", "❌ Not available", "Install docker package")
            
    except ImportError:
        table.add_row("Firebolt SDK", "❌ Not installed", "-")
    
    console.print(table)
    console.print("\n🎯 Run [bold]dreambolt ingest --help[/bold] to get started!")
    console.print("🐳 Run [bold]dreambolt firebolt setup[/bold] to setup free Firebolt Core!")


# Create separate Typer app for Firebolt commands
firebolt_app = typer.Typer(name="firebolt", help="🔥 Firebolt Core management commands")

# Add Firebolt app as a subcommand
app.add_typer(firebolt_app, name="firebolt")


@firebolt_app.command("setup")
def setup_firebolt_core_cmd():
    """🚀 Set up Firebolt Core infrastructure."""
    console.print("🚀 [bold]Setting up Firebolt Core[/bold]")
    console.print("This will pull and start the free, self-hosted Firebolt Core container.")
    
    try:
        connector = setup_firebolt_core()
        
        # Show status after setup
        status = connector.core_status()
        
        console.print("✅ [bold green]Firebolt Core setup completed![/bold green]")
        console.print(f"🐳 Container: {status.get('container_id', 'N/A')}")
        console.print(f"🔌 Port: {status.get('port', 'N/A')}")
        console.print(f"🗄️  Database: {status.get('database', 'N/A')}")
        console.print("\n🎯 You can now run: [bold]dreambolt ingest your-data.csv[/bold]")
        
    except Exception as e:
        console.print(f"❌ [bold red]Setup failed:[/bold red] {str(e)}")
        console.print("🔧 Make sure Docker is installed and running:")
        console.print("   • Install Docker: https://docs.docker.com/get-docker/")
        console.print("   • Start Docker service")
        console.print("   • Run: docker --version")
        raise typer.Exit(1)


@firebolt_app.command("status")
def firebolt_status_cmd():
    """📊 Show Firebolt Core status and information."""
    try:
        from firebolt_io_simple import FireboltConnector
        
        connector = FireboltConnector()
        status = connector.core_status()
        
        # Create detailed status table
        table = Table(title="Firebolt Core Status")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Backend", status.get("backend", "unknown"))
        table.add_row("Status", status.get("status", "unknown"))
        table.add_row("Container ID", status.get("container_id", "N/A"))
        table.add_row("Image", status.get("image", "N/A"))
        table.add_row("Port", str(status.get("port", "N/A")))
        table.add_row("Connection", status.get("connection", "N/A"))
        table.add_row("Database", status.get("database", "N/A"))
        table.add_row("Version", status.get("version", "N/A"))
        
        console.print(table)
        
        if status.get("status") == "not_created":
            console.print("\n💡 Run [bold]dreambolt firebolt setup[/bold] to create Firebolt Core")
        elif status.get("status") == "running" and status.get("connection") == "connected":
            console.print("\n✅ Firebolt Core is ready for data ingestion!")
        
    except Exception as e:
        console.print(f"❌ [bold red]Status check failed:[/bold red] {str(e)}")
        raise typer.Exit(1)


@firebolt_app.command("stop")
def stop_firebolt_core_cmd():
    """🛑 Stop Firebolt Core container."""
    try:
        from firebolt_io_simple import FireboltConnector
        
        connector = FireboltConnector()
        if connector.backend == "core":
            connector.stop_core()
            console.print("✅ [bold green]Firebolt Core stopped[/bold green]")
        else:
            console.print("⚠️  [bold yellow]No Firebolt Core instance to stop[/bold yellow]")
            
    except Exception as e:
        console.print(f"❌ [bold red]Stop failed:[/bold red] {str(e)}")
        raise typer.Exit(1)


@firebolt_app.command("query")
def query_firebolt_cmd(
    sql: str = typer.Argument(
        ...,
        help="SQL query to execute"
    ),
    output: Optional[str] = typer.Option(
        None,
        "--output", "-o",
        help="Save results to CSV file"
    )
):
    """📊 Execute SQL query against Firebolt Core."""
    try:
        from firebolt_io_simple import FireboltConnector
        
        connector = FireboltConnector()
        
        if connector.backend != "core":
            console.print("❌ [bold red]Firebolt Core not available[/bold red]")
            console.print("Run: [bold]dreambolt firebolt setup[/bold]")
            raise typer.Exit(1)
        
        # Execute query
        console.print(f"🔍 Executing: [dim]{sql}[/dim]")
        result = connector.query(sql)
        
        if result.empty:
            console.print("📊 Query returned no results")
        else:
            console.print(f"📊 Query returned {len(result)} rows:")
            console.print(result.to_string(index=False))
            
            # Save to file if requested
            if output:
                result.to_csv(output, index=False)
                console.print(f"💾 Results saved to: {output}")
        
    except Exception as e:
        console.print(f"❌ [bold red]Query failed:[/bold red] {str(e)}")
        raise typer.Exit(1)


def version_callback(value: bool):
    """Show version information and exit."""
    if value:
        import platform
        try:
            from importlib.metadata import version
            typer_version = version("typer")
        except Exception:
            typer_version = "unknown"
        
        try:
            from importlib.metadata import version
            click_version = version("click")
        except Exception:
            click_version = "unknown"
        
        console.print(f"🚀 [bold]DreamBolt CLI[/bold]")
        console.print(f"Python: {platform.python_version()}")
        console.print(f"Typer: {typer_version}")
        console.print(f"Click: {click_version}")
        console.print(f"Platform: {platform.system()} {platform.machine()}")
        console.print(f"")
        console.print(f"🔥 Firebolt Core: Free self-hosted analytics")
        console.print(f"📖 Docs: https://docs.firebolt.io/firebolt-core")
        raise typer.Exit()


# Add version option to the main app
@app.callback()
def main(
    version: bool = typer.Option(
        False, 
        "--version", 
        callback=version_callback, 
        is_eager=True,
        help="Show version information and exit"
    )
):
    """🚀 DreamBolt: AI-powered data ingestion and synthesis pipeline with Firebolt Core"""
    pass


def _generate_output_path(input_path: str) -> str:
    """Generate output path from input path."""
    input_file = Path(input_path)
    if input_file.suffix.lower() in ['.csv', '.parquet']:
        return str(input_file.with_suffix('.dreambolt.parquet'))
    else:
        return f"{input_path}.dreambolt.parquet"


def _derive_table_name(input_path: str) -> str:
    """Derive Firebolt table name from input path."""
    input_file = Path(input_path)
    base_name = input_file.stem
    # Clean up for SQL table naming
    return base_name.replace('-', '_').replace(' ', '_').lower()


if __name__ == "__main__":
    # Local smoke test - only run when called directly
    app()

# ⬇️ COMMIT SUGGESTION: git add -A && git commit -m "feat: add Firebolt Core integration with Docker support" 