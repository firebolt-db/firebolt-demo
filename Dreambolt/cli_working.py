#!/usr/bin/env python3
"""
DreamBolt CLI - Working version using argparse.
Bypasses typer/rich compatibility issues with Python 3.13.
"""
import argparse
import sys
from pathlib import Path

from ingest_simple import DataIngester
from synth_simple import DataSynthesizer
from firebolt_io_simple import FireboltConnector


def status_command():
    """Check DreamBolt and dependency status."""
    print("🚀 DreamBolt Status Check")
    
    # Check dependencies
    try:
        import pandas
        print(f"✅ Pandas: {pandas.__version__}")
    except ImportError:
        print("❌ Pandas: Not installed")
    
    try:
        from synth_simple import DataSynthesizer
        # Test that we can access it  
        _ = DataSynthesizer.__name__  # Use the import
        print("✅ DataDreamer: Available (fallback mode)")
    except ImportError:
        print("❌ DataDreamer: Not installed")
    
    try:
        from firebolt_io_simple import FireboltConnector
        # Test that we can access it
        _ = FireboltConnector.__name__  # Use the import
        print("✅ Firebolt SDK: Available (simulation mode)")
    except ImportError:
        print("❌ Firebolt SDK: Not installed")
    
    print("\n🎯 Run 'python cli_working.py ingest --help' to get started!")


def ingest_command(args):
    """Ingest data with optional synthesis."""
    print(f"🚀 Starting DreamBolt ingestion: {args.input_path}")
    
    try:
        # Step 1: Data Ingestion
        print("⠋ Loading and analyzing data...")
        ingester = DataIngester()
        df, schema_info = ingester.load_data(args.input_path)
        print(f"📊 Loaded {len(df)} rows, {len(df.columns)} columns")
        
        # Step 2: Schema Cleaning
        print("⠋ Cleaning schema...")
        cleaned_df = ingester.clean_schema(df, schema_info)
        print("🧹 Schema cleaned and validated")
        
        # Step 3: Optional Synthesis
        final_df = cleaned_df
        if not args.no_synth and args.synthesize:
            print(f"⠋ Synthesizing {args.synthesize} rows...")
            synthesizer = DataSynthesizer(model=args.model)
            final_df = synthesizer.synthesize_rows(cleaned_df, count=args.synthesize)
            print(f"🤖 Generated {args.synthesize} synthetic rows")
        
        # Step 4: Optional Embeddings
        if args.embed:
            print("⠋ Generating embeddings...")
            synthesizer = DataSynthesizer()
            final_df = synthesizer.add_embeddings(final_df, args.embed)
            print("🔢 Added embedding columns")
        
        # Step 5: Output Processing
        print("⠋ Writing output files...")
        output_path = args.output or _generate_output_path(args.input_path)
        final_df.to_parquet(output_path)
        print(f"💾 Saved to: {output_path}")
        
        # Step 6: Firebolt Integration
        if not args.dry_run:
            print("⠋ Loading to Firebolt...")
            firebolt = FireboltConnector(engine=args.engine)
            table_name = args.table or _derive_table_name(args.input_path)
            firebolt.ensure_table(table_name, final_df)
            firebolt.copy_data(table_name, output_path)
            print(f"🔥 Data loaded to Firebolt table: {table_name}")
        else:
            print("🔍 Dry run - skipping Firebolt operations")
        
        print("✅ Ingestion completed successfully!")
        
    except Exception as e:
        print(f"❌ Pipeline failed: {str(e)}")
        sys.exit(1)


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
    return base_name.replace('-', '_').replace(' ', '_').lower()


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="🚀 DreamBolt: AI-powered data ingestion and synthesis pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Status command
    _status_parser = subparsers.add_parser('status', help='Check DreamBolt status')
    
    # Ingest command
    ingest_parser = subparsers.add_parser('ingest', help='Ingest and process data')
    ingest_parser.add_argument('input_path', help='Input data path (CSV/Parquet file)')
    ingest_parser.add_argument('--output', '-o', help='Output Parquet file path')
    ingest_parser.add_argument('--table', '-t', help='Firebolt table name')
    ingest_parser.add_argument('--no-synth', action='store_true', help='Skip synthesis step')
    ingest_parser.add_argument('--synthesize', '-s', type=int, help='Number of synthetic rows to generate')
    ingest_parser.add_argument('--model', '-m', default='openai:gpt-3.5-turbo', help='LLM model for synthesis')
    ingest_parser.add_argument('--embed', help='Generate embeddings using specified model')
    ingest_parser.add_argument('--engine', help='Firebolt engine name')
    ingest_parser.add_argument('--dry-run', action='store_true', help='Show what would be done without executing')
    ingest_parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    if args.command == 'status':
        status_command()
    elif args.command == 'ingest':
        ingest_command(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main() 