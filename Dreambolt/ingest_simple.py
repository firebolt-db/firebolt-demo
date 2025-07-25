"""
Simplified data ingestion module for DreamBolt.
Handles CSV/Parquet loading and schema inference (no S3 for now).
"""
import pandas as pd
from pathlib import Path
from typing import Tuple, Dict
from loguru import logger
from pydantic import BaseModel


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
    """Main data ingestion class with local file support."""
    
    def __init__(self):
        self.supported_formats = {'.csv', '.parquet', '.pqt'}
    
    def load_data(self, path: str) -> Tuple[pd.DataFrame, SchemaInfo]:
        """
        Load data from local file.
        
        Args:
            path: Local file path
            
        Returns:
            Tuple of (DataFrame, SchemaInfo)
        """
        logger.info(f"Loading data from: {path}")
        
        if path.startswith('s3://'):
            raise NotImplementedError("S3 support temporarily disabled. Use local files.")
        
        return self._load_from_local(path)
    
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
        """Optimize DataFrame data types for memory efficiency."""
        optimized_df = df.copy()
        
        for col in optimized_df.columns:
            col_type = optimized_df[col].dtype
            
            # Optimize integer columns
            if pd.api.types.is_integer_dtype(col_type):
                min_val = optimized_df[col].min()
                max_val = optimized_df[col].max()
                
                if min_val >= 0 and max_val <= 255:
                    optimized_df[col] = optimized_df[col].astype('uint8')
                elif min_val >= -128 and max_val <= 127:
                    optimized_df[col] = optimized_df[col].astype('int8')
                elif min_val >= 0 and max_val <= 65535:
                    optimized_df[col] = optimized_df[col].astype('uint16')
                elif min_val >= -32768 and max_val <= 32767:
                    optimized_df[col] = optimized_df[col].astype('int16')
        
        return optimized_df


if __name__ == "__main__":
    # Smoke test
    import tempfile
    test_data = pd.DataFrame({
        'id': [1, 2, 3],
        'name': ['Alice', 'Bob', 'Charlie'],
        'score': [95.5, 87.2, 92.8]
    })
    
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
        test_data.to_csv(f.name, index=False)
        
        ingester = DataIngester()
        df, schema_info = ingester.load_data(f.name)
        cleaned_df = ingester.clean_schema(df, schema_info)
        
        print(f"✅ Smoke test passed: {len(cleaned_df)} rows, {len(cleaned_df.columns)} columns")
        print(f"Potential issues: {schema_info.potential_issues}") 