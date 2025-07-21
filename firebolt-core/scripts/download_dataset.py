#!/usr/bin/env python3
"""
Download and prepare NYC Parking Violations dataset for Firebolt Core demo.

This script downloads the NYC Parking Violations dataset from NYC Open Data
and prepares it for loading into Firebolt Core.
"""

import argparse
import logging
import sys
from pathlib import Path

import pandas as pd
import requests

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Dataset URLs and metadata
DATASETS = {
    "nyc_parking_2019": {
        "url": "https://data.cityofnewyork.us/api/views/faiq-9dfq/rows.csv?accessType=DOWNLOAD",
        "name": "NYC Parking Violations 2019",
        "size_gb": 1.2,
    },
    "nyc_parking_2020": {
        "url": "https://data.cityofnewyork.us/api/views/pvqr-7yc4/rows.csv?accessType=DOWNLOAD",
        "name": "NYC Parking Violations 2020",
        "size_gb": 1.1,
    },
    "nyc_parking_2021": {
        "url": "https://data.cityofnewyork.us/api/views/kvfd-bves/rows.csv?accessType=DOWNLOAD",
        "name": "NYC Parking Violations 2021",
        "size_gb": 1.3,
    },
    "sample": {
        "url": "s3://firebolt-sample-datasets-public-us-east-1/nyc_sample_datasets/nycparking/parquet/",
        "name": "NYC Parking Violations Sample (Parquet)",
        "size_gb": 0.5,
    },
}


class DatasetDownloader:
    """Downloads and processes NYC parking violations dataset."""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

    def download_file(self, url: str, filename: str) -> bool:
        """Download a file with progress tracking."""
        filepath = self.data_dir / filename

        if filepath.exists():
            logger.info(f"File {filename} already exists, skipping download")
            return True

        try:
            logger.info(f"Downloading {filename}...")
            response = requests.get(url, stream=True)
            response.raise_for_status()

            total_size = int(response.headers.get("content-length", 0))

            with open(filepath, "wb") as file:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            print(f"\rProgress: {progress:.1f}%", end="", flush=True)

            print()  # New line after progress
            logger.info(f"Successfully downloaded {filename}")
            return True

        except Exception as e:
            logger.error(f"Failed to download {filename}: {e}")
            return False

    def clean_dataset(self, input_file: str, output_file: str) -> bool:
        """Clean and prepare the dataset for Firebolt."""
        try:
            logger.info(f"Cleaning dataset {input_file}...")

            # Read the CSV file in chunks to handle large files
            chunk_list = []
            chunk_size = 50000

            for chunk in pd.read_csv(
                self.data_dir / input_file,
                chunksize=chunk_size,
                low_memory=False,
                parse_dates=[
                    "Issue Date",
                    "Vehicle Expiration Date",
                    "Date First Observed",
                ],
                date_parser=lambda x: pd.to_datetime(x, errors="coerce"),
            ):
                # Clean the data
                chunk = self.clean_chunk(chunk)
                chunk_list.append(chunk)

            # Combine all chunks
            df = pd.concat(chunk_list, ignore_index=True)

            # Save cleaned data
            output_path = self.data_dir / output_file
            df.to_csv(output_path, index=False)

            logger.info(f"Cleaned dataset saved to {output_file}")
            logger.info(f"Processed {len(df):,} rows")

            return True

        except Exception as e:
            logger.error(f"Failed to clean dataset: {e}")
            return False

    def clean_chunk(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean a chunk of the dataset."""
        # Handle missing values
        df = df.dropna(subset=["Summons Number", "Issue Date"])

        # Clean numeric columns
        if "Fine Amount" in df.columns:
            df["Fine Amount"] = pd.to_numeric(df["Fine Amount"], errors="coerce")
            df["Fine Amount"] = df["Fine Amount"].fillna(0)

        # Clean string columns
        string_columns = df.select_dtypes(include=["object"]).columns
        for col in string_columns:
            if col not in [
                "Issue Date",
                "Vehicle Expiration Date",
                "Date First Observed",
            ]:
                df[col] = df[col].astype(str).str.strip().replace("nan", "")

        return df

    def get_dataset_info(self) -> dict:
        """Get information about available datasets."""
        return DATASETS

    def download_sample_data(self) -> bool:
        """Download a smaller sample dataset for testing."""
        logger.info("Using Firebolt sample dataset from S3...")
        logger.info("This dataset will be loaded directly via SQL COPY INTO command")
        logger.info("No local download required - data is accessed directly from S3")

        # Create a metadata file
        metadata = {
            "source": "Firebolt Sample Datasets",
            "location": "s3://firebolt-sample-datasets-public-us-east-1/nyc_sample_datasets/nycparking/parquet/",
            "format": "parquet",
            "estimated_size": "500MB",
            "estimated_rows": "~2-5 million",
        }

        import json

        with open(self.data_dir / "dataset_metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)

        logger.info("Dataset metadata saved to data/dataset_metadata.json")
        return True


def main():
    parser = argparse.ArgumentParser(
        description="Download NYC Parking Violations dataset"
    )
    parser.add_argument(
        "--dataset",
        choices=["sample", "full"],
        default="sample",
        help="Dataset to download (default: sample)",
    )
    parser.add_argument(
        "--data-dir",
        default="data",
        help="Directory to store data files (default: data)",
    )

    args = parser.parse_args()

    downloader = DatasetDownloader(args.data_dir)

    if args.dataset == "sample":
        success = downloader.download_sample_data()
    else:
        logger.info("Full dataset download not implemented yet.")
        logger.info("Using sample dataset instead...")
        success = downloader.download_sample_data()

    if success:
        logger.info("✅ Dataset preparation completed successfully!")
        logger.info("🚀 You can now run the data loading SQL scripts")
    else:
        logger.error("❌ Dataset preparation failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
