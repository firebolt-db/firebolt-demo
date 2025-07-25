"""
Simplified synthesis module for DreamBolt.
Provides fallback data synthesis without external LLM dependencies.
"""
import pandas as pd
import numpy as np
from typing import Optional, Dict
from loguru import logger


class ModelConfig:
    """Configuration for different LLM models (simplified)."""
    
    SUPPORTED_MODELS = {
        'openai:gpt-3.5-turbo': {'provider': 'openai', 'model': 'gpt-3.5-turbo'},
        'openai:gpt-4': {'provider': 'openai', 'model': 'gpt-4'},
        'openai:gpt-4-turbo': {'provider': 'openai', 'model': 'gpt-4-turbo'},
        'mistralai/Mistral-7B': {'provider': 'huggingface', 'model': 'mistralai/Mistral-7B-v0.1'},
        'microsoft/DialoGPT-medium': {'provider': 'huggingface', 'model': 'microsoft/DialoGPT-medium'}
    }
    
    @classmethod
    def get_model_config(cls, model_name: str) -> Dict[str, str]:
        """Get configuration for a model name."""
        if model_name in cls.SUPPORTED_MODELS:
            return cls.SUPPORTED_MODELS[model_name]
        else:
            # Try to parse custom format: provider:model
            if ':' in model_name:
                provider, model = model_name.split(':', 1)
                return {'provider': provider, 'model': model}
            else:
                return {'provider': 'fallback', 'model': 'simple'}


class DataSynthesizer:
    """Simplified data synthesizer with fallback implementation."""
    
    def __init__(self, model: str = "openai:gpt-3.5-turbo", custom_prompt: Optional[str] = None):
        """
        Initialize DataSynthesizer.
        
        Args:
            model: Model identifier (ignored in simplified version)
            custom_prompt: Custom prompt template (ignored in simplified version)
        """
        self.model_name = model
        self.model_config = ModelConfig.get_model_config(model)
        logger.info("Initialized simplified synthesizer (fallback mode)")
    
    def synthesize_rows(self, df: pd.DataFrame, count: int = 10) -> pd.DataFrame:
        """
        Synthesize new rows using simple statistical methods.
        
        Args:
            df: Source DataFrame
            count: Number of rows to synthesize
            
        Returns:
            DataFrame with original + synthesized rows
        """
        logger.info(f"🎭 Generating {count} synthetic rows using statistical fallback")
        
        if len(df) == 0:
            logger.warning("Empty DataFrame - cannot synthesize")
            return df
        
        # Simple synthesis strategy: sample with variation
        synthesized_rows = []
        
        for i in range(count):
            # Start with a random sample from existing data
            base_row = df.sample(n=1).iloc[0].copy()
            
            # Add some variation to numerical columns
            for col in df.columns:
                if pd.api.types.is_numeric_dtype(df[col]):
                    # Add random noise based on column statistics
                    std = df[col].std()
                    
                    if pd.notna(std) and std > 0:
                        # Add random variation (±10% of std)
                        noise = np.random.normal(0, std * 0.1)
                        base_row[col] = max(0, base_row[col] + noise)  # Keep non-negative
                
                elif df[col].dtype == 'object':
                    # For categorical/string columns, occasionally pick a different value
                    if np.random.random() < 0.3:  # 30% chance to vary
                        unique_vals = df[col].dropna().unique()
                        if len(unique_vals) > 1:
                            base_row[col] = np.random.choice(unique_vals)
            
            synthesized_rows.append(base_row)
        
        # Create synthesized DataFrame
        synthesized_df = pd.DataFrame(synthesized_rows)
        
        # Combine with original data
        combined_df = pd.concat([df, synthesized_df], ignore_index=True)
        
        logger.info(f"✅ Successfully synthesized {len(synthesized_df)} rows")
        return combined_df
    
    def add_embeddings(self, df: pd.DataFrame, embedding_model: str = "text-embedding-ada-002") -> pd.DataFrame:
        """
        Add mock embeddings (simplified version).
        
        Args:
            df: Input DataFrame
            embedding_model: Model name (ignored in simplified version)
            
        Returns:
            DataFrame with mock embedding columns
        """
        logger.info("🎭 Adding mock embeddings (fallback mode)")
        
        # Create mock embedding columns
        embedding_df = df.copy()
        
        # Find text columns for embedding
        text_columns = []
        for col in df.columns:
            if df[col].dtype == 'object':
                text_columns.append(col)
        
        if text_columns:
            # Create a simple mock embedding (random values for demo)
            np.random.seed(42)  # For reproducibility
            mock_embedding = np.random.randn(len(df), 384).tolist()  # 384-dim like sentence transformers
            
            embedding_df['text_embedding'] = mock_embedding
            logger.info("Added mock text_embedding column (384 dimensions)")
        else:
            logger.info("No text columns found for embedding")
        
        return embedding_df


def get_column_info(df: pd.DataFrame) -> str:
    """Get column information for prompts."""
    info_lines = []
    for col, dtype in df.dtypes.items():
        unique_count = df[col].nunique()
        null_count = df[col].isnull().sum()
        info_lines.append(f"- {col}: {dtype} ({unique_count} unique, {null_count} nulls)")
    
    return "\n".join(info_lines)


if __name__ == "__main__":
    # Smoke test
    print("🧪 Running simplified DataSynthesizer smoke test...")
    
    # Create test data
    test_df = pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
        'age': [25, 30, 35, 28, 32],
        'salary': [50000, 60000, 70000, 55000, 65000],
        'department': ['Engineering', 'Sales', 'Engineering', 'Marketing', 'Sales']
    })
    
    synthesizer = DataSynthesizer()
    
    # Test synthesis
    result = synthesizer.synthesize_rows(test_df, count=3)
    print(f"✅ Original: {len(test_df)} rows → Combined: {len(result)} rows")
    
    # Test embeddings
    with_embeddings = synthesizer.add_embeddings(test_df)
    print(f"✅ Added embeddings: {list(with_embeddings.columns)}")
    
    print("✅ Smoke test passed!") 