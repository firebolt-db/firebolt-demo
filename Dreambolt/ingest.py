"""
Data ingestion module for DreamBolt.
Handles CSV/Parquet loading, S3 URIs, and schema inference.
"""
import pandas as pd
from pathlib import Path
from typing import Tuple, Dict
from loguru import logger
from pydantic import BaseModel

# Robust S3 support
try:
    from src.utils.s3_client import (
        S3Client, 
        S3File, 
        is_s3_uri,
        S3BaseError,
        S3AuthError,
        S3NotFoundError,
        S3RateLimitError,
        S3GenericError
    )
    S3_AVAILABLE = True
    logger.info("S3 support enabled with robust error handling")
except ImportError:
    logger.info("S3 dependencies not available - S3 URIs will not be supported")
    S3_AVAILABLE = False


class SchemaInfo(BaseModel):
    """Schema information for loaded data."""
    column_types: Dict[str, str]
    null_counts: Dict[str, int]
    unique_counts: Dict[str, int]
    sample_values: Dict[str, list]
    inferred_categorical: list
    potential_issues: list
    
    class Config:
        arbitrary_types_allowed = True


class DataIngester:
    """Main data ingestion class with multi-format support."""
    
    def __init__(self):
        self.supported_formats = {'.csv', '.parquet', '.pqt'}
        self.s3_client = S3Client() if S3_AVAILABLE else None
    
    def load_data(self, path: str) -> Tuple[pd.DataFrame, SchemaInfo]:
        """
        Load data from local file or S3 URI.
        
        Args:
            path: Local file path or S3 URI (s3://bucket/key)
            
        Returns:
            Tuple of (DataFrame, SchemaInfo)
        """
        logger.info(f"Loading data from: {path}")
        
        if self._is_s3_uri(path):
            return self._load_from_s3(path)
        else:
            return self._load_from_local(path)
    
    def _is_s3_uri(self, path: str) -> bool:
        """Check if path is an S3 URI."""
        return is_s3_uri(path) if S3_AVAILABLE else path.startswith('s3://')
    
    def _load_from_local(self, path: str) -> Tuple[pd.DataFrame, SchemaInfo]:
        """Load data from local file system."""
        file_path = Path(path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        
        if file_path.suffix.lower() not in self.supported_formats:
            raise ValueError(f"Unsupported format: {file_path.suffix}")
        
        # Load based on file extension
        if file_path.suffix.lower() == '.csv':
            df = pd.read_csv(path)
        elif file_path.suffix.lower() in ['.parquet', '.pqt']:
            df = pd.read_parquet(path)
        else:
            raise ValueError(f"Unsupported format: {file_path.suffix}")
        
        logger.info(f"Loaded {len(df)} rows, {len(df.columns)} columns")
        schema_info = self._analyze_schema(df)
        
        return df, schema_info
    
    def _load_from_s3(self, s3_uri: str) -> Tuple[pd.DataFrame, SchemaInfo]:
        """Load data from S3 with robust error handling and progress tracking."""
        if not S3_AVAILABLE:
            raise ImportError("S3 functionality requires boto3, s3fs, and tqdm packages. Install with: pip install boto3 s3fs tqdm")
        
        if not self.s3_client:
            raise RuntimeError("S3 client not initialized")
        
        try:
            # Parse S3 URI and get metadata
            bucket, key, region = self.s3_client.parse_s3_uri(s3_uri)
            logger.info(f"Loading from S3: bucket={bucket}, key={key}, region={region}")
            
            # Check if file exists
            if not self.s3_client.exists(s3_uri):
                raise FileNotFoundError(f"S3 object not found: {s3_uri}")
            
            # Determine file type from extension
            if key.endswith('.csv'):
                logger.info("Loading CSV file from S3...")
                with S3File(s3_uri, mode='r', client=self.s3_client) as f:
                    df = pd.read_csv(f)
            elif key.endswith(('.parquet', '.pqt')):
                logger.info("Loading Parquet file from S3...")
                # For parquet, we use the s3fs filesystem directly with pandas
                fs = self.s3_client._get_filesystem()
                df = pd.read_parquet(s3_uri, filesystem=fs)
            else:
                raise ValueError(f"Unsupported S3 file format: {key}")
            
            logger.info(f"Successfully loaded {len(df)} rows, {len(df.columns)} columns from S3")
            schema_info = self._analyze_schema(df)
            
            return df, schema_info
            
        except S3AuthError as e:
            logger.error(f"S3 authentication error: {e}")
            raise
        except S3NotFoundError as e:
            logger.error(f"S3 file not found: {e}")
            raise FileNotFoundError(f"S3 file not found: {s3_uri}") from e
        except S3RateLimitError as e:
            logger.error(f"S3 rate limit exceeded: {e}")
            raise
        except S3GenericError as e:
            logger.error(f"S3 error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error loading from S3: {e}")
            raise RuntimeError(f"Failed to load data from S3: {e}") from e
    
    def _analyze_schema(self, df: pd.DataFrame) -> SchemaInfo:
        """Perform comprehensive schema analysis."""
        logger.debug("Analyzing schema and data characteristics")
        
        # Basic type information
        column_types = df.dtypes.astype(str).to_dict()
        null_counts = df.isnull().sum().to_dict()
        unique_counts = df.nunique().to_dict()
        
        # Sample values for each column
        sample_values = {}
        for col in df.columns:
            # Get up to 5 non-null sample values
            samples = df[col].dropna().head(5).tolist()
            sample_values[col] = samples
        
        # Infer categorical columns
        inferred_categorical = []
        for col in df.columns:
            if df[col].dtype == 'object':  # String columns
                unique_ratio = df[col].nunique() / len(df)
                if unique_ratio < 0.1 or df[col].nunique() < 20:
                    inferred_categorical.append(col)
        
        # Identify potential issues
        potential_issues = []
        for col in df.columns:
            null_pct = (null_counts[col] / len(df)) * 100
            if null_pct > 50:
                potential_issues.append(f"Column '{col}' has {null_pct:.1f}% null values")
            
            if df[col].dtype == 'object' and unique_counts[col] == len(df):
                potential_issues.append(f"Column '{col}' appears to be all unique (potential ID column)")
        
        return SchemaInfo(
            column_types=column_types,
            null_counts=null_counts,
            unique_counts=unique_counts,
            sample_values=sample_values,
            inferred_categorical=inferred_categorical,
            potential_issues=potential_issues
        )
    
    def clean_schema(self, df: pd.DataFrame, schema_info: SchemaInfo) -> pd.DataFrame:
        """
        Clean and standardize the schema based on analysis.
        
        Args:
            df: Input DataFrame
            schema_info: Schema analysis results
            
        Returns:
            Cleaned DataFrame
        """
        logger.info("Cleaning and standardizing schema")
        cleaned_df = df.copy()
        
        # 1. Handle column names (standardize)
        cleaned_df.columns = [self._clean_column_name(col) for col in cleaned_df.columns]
        
        # 2. Convert inferred categorical columns
        for col in schema_info.inferred_categorical:
            clean_col = self._clean_column_name(col)
            if clean_col in cleaned_df.columns:
                logger.debug(f"Converting '{clean_col}' to categorical")
                cleaned_df[clean_col] = cleaned_df[clean_col].astype('category')
        
        # 3. Handle missing values strategically
        for col in cleaned_df.columns:
            null_pct = (cleaned_df[col].isnull().sum() / len(cleaned_df)) * 100
            if null_pct > 90:
                logger.warning(f"Dropping column '{col}' - {null_pct:.1f}% null values")
                cleaned_df = cleaned_df.drop(columns=[col])
        
        # 4. Basic data type optimization
        cleaned_df = self._optimize_dtypes(cleaned_df)
        
        logger.info(f"Schema cleaning complete: {len(cleaned_df.columns)} columns retained")
        return cleaned_df
    
    def _clean_column_name(self, name: str) -> str:
        """Standardize column names for SQL compatibility."""
        # Convert to lowercase, replace spaces/special chars with underscores
        clean_name = name.lower().strip()
        clean_name = ''.join(c if c.isalnum() else '_' for c in clean_name)
        # Remove consecutive underscores
        while '__' in clean_name:
            clean_name = clean_name.replace('__', '_')
        clean_name = clean_name.strip('_')
        
        # Ensure it starts with a letter
        if clean_name and clean_name[0].isdigit():
            clean_name = f'col_{clean_name}'
        
        return clean_name or 'unnamed_column'
    
    def _optimize_dtypes(self, df: pd.DataFrame) -> pd.DataFrame:
        """Optimize data types for memory efficiency."""
        optimized_df = df.copy()
        
        for col in optimized_df.columns:
            if optimized_df[col].dtype == 'int64':
                # Try to downcast integers
                col_min = optimized_df[col].min()
                col_max = optimized_df[col].max()
                
                if col_min >= 0:  # Unsigned integers
                    if col_max < 255:
                        optimized_df[col] = optimized_df[col].astype('uint8')
                    elif col_max < 65535:
                        optimized_df[col] = optimized_df[col].astype('uint16')
                    elif col_max < 4294967295:
                        optimized_df[col] = optimized_df[col].astype('uint32')
                else:  # Signed integers
                    if col_min > -128 and col_max < 127:
                        optimized_df[col] = optimized_df[col].astype('int8')
                    elif col_min > -32768 and col_max < 32767:
                        optimized_df[col] = optimized_df[col].astype('int16')
                    elif col_min > -2147483648 and col_max < 2147483647:
                        optimized_df[col] = optimized_df[col].astype('int32')
            
            elif optimized_df[col].dtype == 'float64':
                # Try to downcast floats
                optimized_df[col] = pd.to_numeric(optimized_df[col], downcast='float')
        
        return optimized_df


if __name__ == "__main__":
    # Local smoke test
    print("🧪 Running DataIngester smoke test...")
    
    # Create test CSV
    import tempfile
    test_data = pd.DataFrame({
        'ID': [1, 2, 3, 4, 5],
        'Name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
        'Age': [25, 30, 35, 28, 32],
        'Department': ['Engineering', 'Sales', 'Engineering', 'HR', 'Sales']
    })
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        test_data.to_csv(f.name, index=False)
        test_file = f.name
    
    try:
        ingester = DataIngester()
        df, schema_info = ingester.load_data(test_file)
        cleaned_df = ingester.clean_schema(df, schema_info)
        
        print(f"✅ Loaded and cleaned {len(cleaned_df)} rows")
        print(f"✅ Schema analysis: {len(schema_info.potential_issues)} issues found")
        print("✅ Smoke test passed!")
        
    finally:
        Path(test_file).unlink(missing_ok=True)

# ⬇️ COMMIT SUGGESTION: git add -A && git commit -m "feat: add data ingestion with schema inference" 