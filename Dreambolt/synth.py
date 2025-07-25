"""
DataDreamer synthesis module for DreamBolt.
Handles LLM-powered data synthesis and embedding generation.
"""
import pandas as pd
import numpy as np
from typing import Optional, Dict, List
import os
from loguru import logger

# DataDreamer imports
try:
    from datadreamer import DataDreamer
    from datadreamer.llms import OpenAI, HuggingFaceLLM
    from datadreamer.steps import ProcessWithLLM, Prompt
    DATADREAMER_AVAILABLE = True
except ImportError:
    logger.info("DataDreamer not available - synthesis features will use fallback")
    DATADREAMER_AVAILABLE = False
    # Create dummy classes to prevent import errors
    class DataDreamer:
        def __init__(self, *args, **kwargs):
            pass
        def __enter__(self):
            return self
        def __exit__(self, *args):
            pass
    
    class OpenAI:
        def __init__(self, *args, **kwargs):
            pass
    
    class HuggingFaceLLM:
        def __init__(self, *args, **kwargs):
            pass

# OpenAI for embeddings
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    logger.warning("OpenAI not available - embedding features disabled")
    OPENAI_AVAILABLE = False


# Prompt Engineering Templates
DEFAULT_PROMPT = """
You are a data synthesis expert. Given the following data sample, generate {count} new rows that follow the same patterns and distributions.

IMPORTANT INSTRUCTIONS:
- Maintain the same column structure and data types
- Follow realistic patterns from the sample data
- Ensure categorical values match existing categories when appropriate
- Keep numerical values within reasonable ranges based on samples
- Generate diverse but realistic data

Sample Data:
{sample_rows}

Column Information:
{column_info}

Generate {count} new rows in the same CSV format (with headers):
"""

EMBEDDING_PROMPT = """
Create a semantic summary of this data row for embedding generation.
Focus on the key meaningful content that would be useful for similarity matching.

Row data: {row_data}
Summary:
"""

SCHEMA_CLEANING_PROMPT = """
Analyze this data schema and suggest improvements for data quality.

Schema: {schema_info}
Sample Data: {sample_data}

Provide recommendations for:
1. Column name standardization
2. Data type optimization  
3. Missing value handling
4. Categorical encoding

Response:
"""


class ModelConfig:
    """Configuration for different LLM models."""
    
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
                raise ValueError(f"Unsupported model format: {model_name}")


class DataSynthesizer:
    """Main class for data synthesis and embedding generation."""
    
    def __init__(self, model: str = "openai:gpt-3.5-turbo", custom_prompt: Optional[str] = None):
        """
        Initialize DataSynthesizer.
        
        Args:
            model: Model identifier (e.g., 'openai:gpt-3.5-turbo', 'mistralai/Mistral-7B')
            custom_prompt: Custom prompt template (optional)
        """
        self.model_name = model
        self.model_config = ModelConfig.get_model_config(model)
        self.custom_prompt = custom_prompt or DEFAULT_PROMPT
        self.llm = None
        
        if DATADREAMER_AVAILABLE:
            self._initialize_llm()
        else:
            logger.warning("DataDreamer not available - falling back to simple synthesis")
    
    def _initialize_llm(self):
        """Initialize the LLM based on configuration."""
        try:
            if self.model_config['provider'] == 'openai':
                api_key = os.getenv('OPENAI_API_KEY')
                if not api_key:
                    raise ValueError("OPENAI_API_KEY environment variable required for OpenAI models")
                self.llm = OpenAI(model_name=self.model_config['model'], api_key=api_key)
            
            elif self.model_config['provider'] == 'huggingface':
                self.llm = HuggingFaceLLM(model_name=self.model_config['model'])
            
            else:
                raise ValueError(f"Unsupported provider: {self.model_config['provider']}")
            
            logger.info(f"Initialized LLM: {self.model_name}")
            
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            self.llm = None
    
    def synthesize_rows(self, df: pd.DataFrame, count: int = 10) -> pd.DataFrame:
        """
        Synthesize new rows based on existing data.
        
        Args:
            df: Source DataFrame
            count: Number of rows to synthesize
            
        Returns:
            DataFrame with original + synthesized rows
        """
        logger.info(f"Synthesizing {count} rows using {self.model_name}")
        
        if not DATADREAMER_AVAILABLE or self.llm is None:
            logger.warning("Using fallback synthesis (random sampling)")
            return self._fallback_synthesis(df, count)
        
        try:
            with DataDreamer("DreamBolt Synthesis"):
                # Prepare sample data for the prompt
                sample_rows = df.head(min(5, len(df))).to_csv(index=False)
                column_info = self._get_column_info(df)
                
                # Create synthesis prompt
                synthesis_prompt = self.custom_prompt.format(
                    count=count,
                    sample_rows=sample_rows,
                    column_info=column_info
                )
                
                # Run synthesis
                prompt_step = Prompt("synthesis_prompt", text=synthesis_prompt)
                synthesis_step = ProcessWithLLM(
                    "synthesize_data",
                    inputs=prompt_step,
                    llm=self.llm,
                    output_names=["synthesized_data"]
                )
                
                # Parse the synthesized data
                synthesized_text = synthesis_step.output["synthesized_data"][0]
                synthesized_df = self._parse_synthesized_data(synthesized_text, df.columns)
                
                if len(synthesized_df) > 0:
                    # Combine original and synthesized data
                    combined_df = pd.concat([df, synthesized_df], ignore_index=True)
                    logger.info(f"Successfully synthesized {len(synthesized_df)} rows")
                    return combined_df
                else:
                    logger.warning("No valid synthesized data - using fallback")
                    return self._fallback_synthesis(df, count)
        
        except Exception as e:
            logger.error(f"Synthesis failed: {e}")
            return self._fallback_synthesis(df, count)
    
    def _fallback_synthesis(self, df: pd.DataFrame, count: int) -> pd.DataFrame:
        """Fallback synthesis using statistical sampling."""
        logger.info("Using statistical synthesis (sampling with noise)")
        
        synthesized_rows = []
        for _ in range(count):
            # Sample a random row and add noise
            base_row = df.sample(1).iloc[0].copy()
            
            for col in df.columns:
                if df[col].dtype in ['int64', 'float64']:
                    # Add small random noise to numeric columns
                    noise_factor = 0.1  # 10% noise
                    original_value = base_row[col]
                    if pd.notna(original_value):
                        noise = np.random.normal(0, abs(original_value) * noise_factor)
                        base_row[col] = original_value + noise
                        
                        # Keep same data type
                        if df[col].dtype == 'int64':
                            base_row[col] = int(round(base_row[col]))
                
                elif df[col].dtype == 'object':
                    # For categorical data, occasionally sample from other values
                    if np.random.random() < 0.3:  # 30% chance to vary
                        unique_values = df[col].dropna().unique()
                        if len(unique_values) > 1:
                            base_row[col] = np.random.choice(unique_values)
            
            synthesized_rows.append(base_row)
        
        synthesized_df = pd.DataFrame(synthesized_rows)
        combined_df = pd.concat([df, synthesized_df], ignore_index=True)
        
        return combined_df
    
    def _get_column_info(self, df: pd.DataFrame) -> str:
        """Generate column information for prompts."""
        info_lines = []
        for col in df.columns:
            dtype = str(df[col].dtype)
            unique_count = df[col].nunique()
            null_count = df[col].isnull().sum()
            
            info_lines.append(f"- {col}: {dtype}, {unique_count} unique values, {null_count} nulls")
            
            # Add sample values for categorical columns
            if df[col].dtype == 'object' and unique_count <= 10:
                sample_values = df[col].dropna().unique()[:5]
                info_lines.append(f"  Sample values: {list(sample_values)}")
        
        return "\n".join(info_lines)
    
    def _parse_synthesized_data(self, text: str, expected_columns: List[str]) -> pd.DataFrame:
        """Parse synthesized data from LLM response."""
        try:
            # Look for CSV-like content in the response
            lines = text.strip().split('\n')
            csv_lines = []
            found_header = False
            
            for line in lines:
                if not found_header and any(col.lower() in line.lower() for col in expected_columns):
                    found_header = True
                    csv_lines.append(line)
                elif found_header and ',' in line:
                    csv_lines.append(line)
            
            if len(csv_lines) > 1:  # Header + at least one data row
                csv_content = '\n'.join(csv_lines)
                df = pd.read_csv(pd.StringIO(csv_content))
                
                # Validate columns match expected
                if set(df.columns) == set(expected_columns):
                    return df
                else:
                    logger.warning("Column mismatch in synthesized data")
            
        except Exception as e:
            logger.error(f"Failed to parse synthesized data: {e}")
        
        return pd.DataFrame()  # Return empty DataFrame on failure
    
    def add_embeddings(self, df: pd.DataFrame, embedding_model: str = "text-embedding-ada-002") -> pd.DataFrame:
        """
        Add embedding columns to the DataFrame.
        
        Args:
            df: Input DataFrame
            embedding_model: OpenAI embedding model name
            
        Returns:
            DataFrame with added embedding columns
        """
        if not OPENAI_AVAILABLE:
            logger.warning("OpenAI not available - skipping embeddings")
            return df
        
        logger.info(f"Generating embeddings using {embedding_model}")
        
        try:
            client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            
            # Create text representations of each row
            text_representations = []
            for _, row in df.iterrows():
                # Create a text summary of the row
                row_text = "; ".join([f"{col}: {val}" for col, val in row.items() if pd.notna(val)])
                text_representations.append(row_text)
            
            # Generate embeddings in batches
            embeddings = []
            batch_size = 100
            
            for i in range(0, len(text_representations), batch_size):
                batch = text_representations[i:i+batch_size]
                response = client.embeddings.create(
                    input=batch,
                    model=embedding_model
                )
                
                batch_embeddings = [item.embedding for item in response.data]
                embeddings.extend(batch_embeddings)
            
            # Add embeddings as new columns
            embedding_df = df.copy()
            embedding_array = np.array(embeddings)
            
            # Add individual embedding dimensions as columns
            for i in range(embedding_array.shape[1]):
                embedding_df[f'embedding_{i:03d}'] = embedding_array[:, i]
            
            logger.info(f"Added {embedding_array.shape[1]} embedding dimensions")
            return embedding_df
            
        except Exception as e:
            logger.error(f"Embedding generation failed: {e}")
            return df


if __name__ == "__main__":
    # Local smoke test
    print("🧪 Running DataSynthesizer smoke test...")
    
    # Create test data
    test_data = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie'],
        'age': [25, 30, 35],
        'department': ['Engineering', 'Sales', 'HR'],
        'salary': [75000, 65000, 70000]
    })
    
    try:
        synthesizer = DataSynthesizer(model="openai:gpt-3.5-turbo")
        
        # Test fallback synthesis (doesn't require API keys)
        result_df = synthesizer._fallback_synthesis(test_data, 2)
        
        print(f"✅ Original data: {len(test_data)} rows")
        print(f"✅ With synthesis: {len(result_df)} rows")
        print("✅ Smoke test passed!")
        
    except Exception as e:
        print(f"❌ Smoke test failed: {e}")

# ⬇️ COMMIT SUGGESTION: git add -A && git commit -m "feat: add DataDreamer synthesis with prompt templates" 