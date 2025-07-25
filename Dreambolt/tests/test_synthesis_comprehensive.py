"""
Comprehensive Data Synthesis Tests
==================================

Tests for all synthesis functionality including LLM and fallback modes.
"""
import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, Mock, MagicMock

from synth import DataSynthesizer, ModelConfig
from synth_simple import DataSynthesizer as SimpleDataSynthesizer
from synth_simple import ModelConfig as SimpleModelConfig


class TestModelConfig:
    """Test model configuration classes."""
    
    def test_model_config_supported_models(self):
        """Test supported model configurations."""
        config = ModelConfig.get_model_config("openai:gpt-3.5-turbo")
        assert config['provider'] == 'openai'
        assert config['model'] == 'gpt-3.5-turbo'
    
    def test_model_config_custom_format(self):
        """Test custom model format parsing."""
        config = ModelConfig.get_model_config("custom:my-model")
        assert config['provider'] == 'custom'
        assert config['model'] == 'my-model'
    
    def test_model_config_unsupported(self):
        """Test handling of unsupported models."""
        config = ModelConfig.get_model_config("unknown-model")
        assert config['provider'] == 'fallback'
        assert config['model'] == 'simple'
    
    def test_simple_model_config(self):
        """Test simple model config."""
        config = SimpleModelConfig.get_model_config("openai:gpt-4")
        assert config['provider'] == 'openai'
        assert config['model'] == 'gpt-4'


class TestDataSynthesizer:
    """Test main DataSynthesizer class."""
    
    def test_initialization_default(self):
        """Test DataSynthesizer default initialization."""
        synthesizer = DataSynthesizer()
        assert synthesizer.model_name == "openai:gpt-3.5-turbo"
        assert synthesizer.custom_prompt is not None
        assert "data synthesis expert" in synthesizer.custom_prompt.lower()
    
    def test_initialization_custom_model(self):
        """Test DataSynthesizer with custom model."""
        synthesizer = DataSynthesizer(model="openai:gpt-4")
        assert synthesizer.model_name == "openai:gpt-4"
        assert synthesizer.model_config['model'] == 'gpt-4'
    
    def test_initialization_custom_prompt(self):
        """Test DataSynthesizer with custom prompt."""
        custom_prompt = "Custom synthesis prompt {sample_rows} {count}"
        synthesizer = DataSynthesizer(custom_prompt=custom_prompt)
        assert synthesizer.custom_prompt == custom_prompt
    
    @patch('synth.DATADREAMER_AVAILABLE', False)
    def test_initialization_without_datadreamer(self):
        """Test initialization when DataDreamer is not available."""
        synthesizer = DataSynthesizer()
        assert synthesizer.llm is None
    
    @patch('synth.DATADREAMER_AVAILABLE', True)
    @patch('synth.OpenAI')
    def test_initialize_llm_openai(self, mock_openai_class):
        """Test LLM initialization for OpenAI."""
        mock_llm = Mock()
        mock_openai_class.return_value = mock_llm
        
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
            synthesizer = DataSynthesizer(model="openai:gpt-3.5-turbo")
            synthesizer._initialize_llm()
            
            mock_openai_class.assert_called_once()
            assert synthesizer.llm == mock_llm
    
    @patch('synth.DATADREAMER_AVAILABLE', True)
    def test_initialize_llm_missing_api_key(self):
        """Test LLM initialization with missing API key."""
        with patch.dict('os.environ', {}, clear=True):
            synthesizer = DataSynthesizer(model="openai:gpt-3.5-turbo")
            synthesizer._initialize_llm()
            
            assert synthesizer.llm is None
    
    @patch('synth.DATADREAMER_AVAILABLE', True)
    @patch('synth.HuggingFaceLLM')
    def test_initialize_llm_huggingface(self, mock_hf_class):
        """Test LLM initialization for HuggingFace."""
        mock_llm = Mock()
        mock_hf_class.return_value = mock_llm
        
        synthesizer = DataSynthesizer(model="mistralai/Mistral-7B")
        synthesizer._initialize_llm()
        
        mock_hf_class.assert_called_once()
        assert synthesizer.llm == mock_llm
    
    def test_synthesize_rows_fallback(self, sample_csv_data):
        """Test synthesis using fallback method."""
        synthesizer = DataSynthesizer()
        synthesizer.llm = None  # Force fallback
        
        result_df = synthesizer.synthesize_rows(sample_csv_data, count=3)
        
        assert isinstance(result_df, pd.DataFrame)
        assert len(result_df) == len(sample_csv_data) + 3
        assert list(result_df.columns) == list(sample_csv_data.columns)
    
    def test_fallback_synthesis_numeric_columns(self, sample_csv_data):
        """Test fallback synthesis with numeric data."""
        synthesizer = DataSynthesizer()
        
        original_len = len(sample_csv_data)
        result_df = synthesizer._fallback_synthesis(sample_csv_data, count=2)
        
        assert len(result_df) == original_len + 2
        
        # Check that numeric columns have reasonable values
        synthesized_ages = result_df['age'].iloc[original_len:].values
        original_ages = sample_csv_data['age'].values
        
        # Synthesized ages should be in reasonable range
        assert all(0 < age < 150 for age in synthesized_ages)
    
    def test_fallback_synthesis_categorical_columns(self, sample_csv_data):
        """Test fallback synthesis with categorical data."""
        synthesizer = DataSynthesizer()
        
        original_len = len(sample_csv_data)
        result_df = synthesizer._fallback_synthesis(sample_csv_data, count=2)
        
        # Check that categorical values are from original set
        synthesized_depts = result_df['department'].iloc[original_len:].values
        original_depts = set(sample_csv_data['department'].unique())
        
        assert all(dept in original_depts for dept in synthesized_depts)
    
    def test_fallback_synthesis_maintains_dtypes(self, sample_csv_data):
        """Test that fallback synthesis maintains data types."""
        synthesizer = DataSynthesizer()
        
        result_df = synthesizer._fallback_synthesis(sample_csv_data, count=2)
        
        # Check that data types are preserved
        for col in sample_csv_data.columns:
            original_dtype = sample_csv_data[col].dtype
            result_dtype = result_df[col].dtype
            
            # Allow some flexibility in numeric types
            if pd.api.types.is_numeric_dtype(original_dtype):
                assert pd.api.types.is_numeric_dtype(result_dtype)
            else:
                assert original_dtype == result_dtype
    
    @patch('synth.DATADREAMER_AVAILABLE', True)
    @patch('synth.DataDreamer')
    def test_synthesize_rows_with_llm(self, mock_datadreamer, sample_csv_data):
        """Test synthesis using LLM."""
        # Setup mocks
        mock_step = Mock()
        mock_step.output = ["id,name,age,salary,department,start_date,is_active,rating\n6,Frank,28,75000,Engineering,2021-01-01,True,4.0\n"]
        
        mock_context = Mock()
        mock_context.__enter__ = Mock(return_value=mock_context)
        mock_context.__exit__ = Mock(return_value=None)
        mock_datadreamer.return_value = mock_context
        
        with patch('synth.ProcessWithLLM') as mock_process:
            mock_process.return_value = mock_step
            
            synthesizer = DataSynthesizer()
            synthesizer.llm = Mock()  # Mock LLM
            
            result_df = synthesizer.synthesize_rows(sample_csv_data, count=1)
            
            assert isinstance(result_df, pd.DataFrame)
            assert len(result_df) >= len(sample_csv_data)
    
    def test_parse_synthesized_data_valid(self):
        """Test parsing valid synthesized data."""
        synthesizer = DataSynthesizer()
        
        csv_text = "id,name,age\n6,Frank,28\n7,Grace,32\n"
        expected_columns = ['id', 'name', 'age']
        
        result_df = synthesizer._parse_synthesized_data(csv_text, expected_columns)
        
        assert isinstance(result_df, pd.DataFrame)
        assert len(result_df) == 2
        assert list(result_df.columns) == expected_columns
        assert 'Frank' in result_df['name'].values
    
    def test_parse_synthesized_data_invalid(self):
        """Test parsing invalid synthesized data."""
        synthesizer = DataSynthesizer()
        
        invalid_text = "This is not CSV data"
        expected_columns = ['id', 'name', 'age']
        
        result_df = synthesizer._parse_synthesized_data(invalid_text, expected_columns)
        
        assert isinstance(result_df, pd.DataFrame)
        assert len(result_df) == 0  # Should return empty DataFrame
    
    def test_parse_synthesized_data_wrong_columns(self):
        """Test parsing data with wrong columns."""
        synthesizer = DataSynthesizer()
        
        csv_text = "wrong,columns\n1,2\n3,4\n"
        expected_columns = ['id', 'name', 'age']
        
        result_df = synthesizer._parse_synthesized_data(csv_text, expected_columns)
        
        assert isinstance(result_df, pd.DataFrame)
        assert len(result_df) == 0  # Should return empty DataFrame
    
    @patch('synth.OPENAI_AVAILABLE', False)
    def test_add_embeddings_without_openai(self, sample_csv_data):
        """Test embedding generation without OpenAI."""
        synthesizer = DataSynthesizer()
        
        result_df = synthesizer.add_embeddings(sample_csv_data)
        
        # Should return original DataFrame unchanged
        pd.testing.assert_frame_equal(result_df, sample_csv_data)
    
    @patch('synth.OPENAI_AVAILABLE', True)
    @patch('synth.openai.OpenAI')
    def test_add_embeddings_with_openai(self, mock_openai_class, sample_csv_data):
        """Test embedding generation with OpenAI."""
        # Setup mock OpenAI client
        mock_client = Mock()
        mock_response = Mock()
        mock_response.data = [
            Mock(embedding=[0.1] * 1536),
            Mock(embedding=[0.2] * 1536),
            Mock(embedding=[0.3] * 1536),
            Mock(embedding=[0.4] * 1536),
            Mock(embedding=[0.5] * 1536)
        ]
        mock_client.embeddings.create.return_value = mock_response
        mock_openai_class.return_value = mock_client
        
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
            synthesizer = DataSynthesizer()
            
            result_df = synthesizer.add_embeddings(sample_csv_data)
            
            assert len(result_df) == len(sample_csv_data)
            assert len(result_df.columns) > len(sample_csv_data.columns)
            
            # Check that embedding columns were added
            embedding_columns = [col for col in result_df.columns if col.startswith('embedding_')]
            assert len(embedding_columns) == 1536  # Standard OpenAI embedding size
    
    @patch('synth.OPENAI_AVAILABLE', True)
    @patch('synth.openai.OpenAI')
    def test_add_embeddings_custom_model(self, mock_openai_class, sample_csv_data):
        """Test embedding generation with custom model."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.data = [Mock(embedding=[0.1] * 512)] * len(sample_csv_data)
        mock_client.embeddings.create.return_value = mock_response
        mock_openai_class.return_value = mock_client
        
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
            synthesizer = DataSynthesizer()
            
            result_df = synthesizer.add_embeddings(sample_csv_data, embedding_model="text-embedding-3-small")
            
            mock_client.embeddings.create.assert_called_once()
            call_args = mock_client.embeddings.create.call_args
            assert call_args[1]['model'] == "text-embedding-3-small"
    
    @patch('synth.OPENAI_AVAILABLE', True)
    @patch('synth.openai.OpenAI')
    def test_add_embeddings_batch_processing(self, mock_openai_class, large_dataset):
        """Test embedding generation with batch processing."""
        mock_client = Mock()
        
        # Mock multiple batch responses
        def mock_create(*args, **kwargs):
            batch_size = len(kwargs['input'])
            mock_response = Mock()
            mock_response.data = [Mock(embedding=[0.1] * 1536)] * batch_size
            return mock_response
        
        mock_client.embeddings.create = mock_create
        mock_openai_class.return_value = mock_client
        
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
            synthesizer = DataSynthesizer()
            
            result_df = synthesizer.add_embeddings(large_dataset)
            
            assert len(result_df) == len(large_dataset)
            # Should have made multiple API calls for large dataset
            assert len(result_df.columns) > len(large_dataset.columns)


class TestSimpleDataSynthesizer:
    """Test simplified DataSynthesizer for fallback scenarios."""
    
    def test_simple_initialization(self):
        """Test SimpleDataSynthesizer initialization."""
        synthesizer = SimpleDataSynthesizer()
        assert synthesizer.model_name == "openai:gpt-3.5-turbo"
    
    def test_simple_fallback_synthesis(self, sample_csv_data):
        """Test simple fallback synthesis."""
        synthesizer = SimpleDataSynthesizer()
        
        result_df = synthesizer._fallback_synthesis(sample_csv_data, count=2)
        
        assert isinstance(result_df, pd.DataFrame)
        assert len(result_df) == len(sample_csv_data) + 2
        assert list(result_df.columns) == list(sample_csv_data.columns)
    
    def test_simple_synthesize_rows(self, sample_csv_data):
        """Test simple synthesize_rows method."""
        synthesizer = SimpleDataSynthesizer()
        
        result_df = synthesizer.synthesize_rows(sample_csv_data, count=3)
        
        assert isinstance(result_df, pd.DataFrame)
        assert len(result_df) == len(sample_csv_data) + 3


class TestSynthesisEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_synthesize_empty_dataframe(self):
        """Test synthesis with empty DataFrame."""
        empty_df = pd.DataFrame()
        synthesizer = DataSynthesizer()
        
        result_df = synthesizer.synthesize_rows(empty_df, count=5)
        
        # Should handle gracefully
        assert isinstance(result_df, pd.DataFrame)
    
    def test_synthesize_single_row(self):
        """Test synthesis with single row DataFrame."""
        single_row_df = pd.DataFrame({'id': [1], 'name': ['Alice']})
        synthesizer = DataSynthesizer()
        
        result_df = synthesizer.synthesize_rows(single_row_df, count=2)
        
        assert len(result_df) == 3
        assert list(result_df.columns) == ['id', 'name']
    
    def test_synthesize_zero_count(self, sample_csv_data):
        """Test synthesis with zero count."""
        synthesizer = DataSynthesizer()
        
        result_df = synthesizer.synthesize_rows(sample_csv_data, count=0)
        
        # Should return original DataFrame
        pd.testing.assert_frame_equal(result_df, sample_csv_data)
    
    def test_synthesize_negative_count(self, sample_csv_data):
        """Test synthesis with negative count."""
        synthesizer = DataSynthesizer()
        
        result_df = synthesizer.synthesize_rows(sample_csv_data, count=-1)
        
        # Should handle gracefully (return original or raise error)
        assert isinstance(result_df, pd.DataFrame)
        assert len(result_df) >= len(sample_csv_data)
    
    def test_synthesize_with_all_null_columns(self):
        """Test synthesis with columns containing only null values."""
        null_df = pd.DataFrame({
            'id': [1, 2, 3],
            'null_column': [None, None, None]
        })
        synthesizer = DataSynthesizer()
        
        result_df = synthesizer._fallback_synthesis(null_df, count=2)
        
        assert len(result_df) == 5
        # Should handle null columns gracefully
    
    def test_synthesize_mixed_types_column(self):
        """Test synthesis with mixed data types in column."""
        mixed_df = pd.DataFrame({
            'id': [1, 2, 3],
            'mixed': [1, 'string', 3.14]
        })
        synthesizer = DataSynthesizer()
        
        result_df = synthesizer._fallback_synthesis(mixed_df, count=2)
        
        assert len(result_df) == 5
        assert 'mixed' in result_df.columns
    
    def test_synthesize_very_large_count(self, sample_csv_data):
        """Test synthesis with very large count."""
        synthesizer = DataSynthesizer()
        
        # This should either work or fail gracefully
        try:
            result_df = synthesizer.synthesize_rows(sample_csv_data, count=10000)
            assert len(result_df) >= len(sample_csv_data)
        except (MemoryError, OverflowError):
            # Expected for very large counts
            pass
    
    def test_embedding_with_empty_dataframe(self):
        """Test embedding generation with empty DataFrame."""
        empty_df = pd.DataFrame()
        synthesizer = DataSynthesizer()
        
        result_df = synthesizer.add_embeddings(empty_df)
        
        # Should handle gracefully
        assert isinstance(result_df, pd.DataFrame)
        assert len(result_df) == 0
    
    def test_embedding_network_error(self, sample_csv_data):
        """Test embedding generation with network error."""
        with patch('synth.OPENAI_AVAILABLE', True), \
             patch('synth.openai.OpenAI') as mock_openai_class:
            
            mock_client = Mock()
            mock_client.embeddings.create.side_effect = ConnectionError("Network error")
            mock_openai_class.return_value = mock_client
            
            synthesizer = DataSynthesizer()
            
            # Should handle network errors gracefully
            try:
                result_df = synthesizer.add_embeddings(sample_csv_data)
                # If it doesn't raise an error, should return original data
                assert len(result_df) == len(sample_csv_data)
            except ConnectionError:
                # Expected behavior - let the error propagate
                pass


class TestSynthesisPerformance:
    """Performance tests for synthesis operations."""
    
    @pytest.mark.slow
    def test_large_dataset_synthesis(self, large_dataset, performance_monitor):
        """Test synthesis with large datasets."""
        synthesizer = DataSynthesizer()
        
        # Use fallback synthesis for deterministic performance
        result_df = synthesizer._fallback_synthesis(large_dataset, count=100)
        
        assert len(result_df) == len(large_dataset) + 100
        assert list(result_df.columns) == list(large_dataset.columns)
    
    def test_synthesis_memory_usage(self, sample_csv_data):
        """Test memory usage during synthesis."""
        synthesizer = DataSynthesizer()
        
        # Get baseline memory usage
        import psutil
        process = psutil.Process()
        start_memory = process.memory_info().rss
        
        result_df = synthesizer.synthesize_rows(sample_csv_data, count=100)
        
        end_memory = process.memory_info().rss
        memory_increase = end_memory - start_memory
        
        # Memory increase should be reasonable
        assert memory_increase < 100 * 1024 * 1024  # Less than 100MB increase
        assert len(result_df) == len(sample_csv_data) + 100
    
    def test_synthesis_deterministic(self, sample_csv_data):
        """Test that synthesis with same seed produces same results."""
        synthesizer = DataSynthesizer()
        
        # Set random seed for reproducibility
        np.random.seed(42)
        result1 = synthesizer._fallback_synthesis(sample_csv_data, count=5)
        
        np.random.seed(42)
        result2 = synthesizer._fallback_synthesis(sample_csv_data, count=5)
        
        # Results should be identical with same seed
        pd.testing.assert_frame_equal(result1, result2) 