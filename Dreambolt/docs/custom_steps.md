# Custom DataDreamer Steps

This guide shows how to extend DreamBolt with custom DataDreamer processing steps for specialized data synthesis and transformation.

## Overview

DreamBolt uses DataDreamer's powerful pipeline system. You can add custom steps to:
- Apply domain-specific synthesis rules
- Add custom data transformations  
- Integrate with external APIs
- Implement custom quality checks

## Basic Custom Step

```python
from datadreamer import DataDreamer
from datadreamer.steps import Step
from synth import DataSynthesizer
import pandas as pd

class CustomFinancialSynthesis(Step):
    """Custom step for financial data synthesis."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def setup(self):
        # Initialize any resources needed
        self.validation_rules = {
            'revenue': lambda x: x > 0,
            'profit_margin': lambda x: 0.05 <= x <= 0.25,
            'employees': lambda x: x > 0 and isinstance(x, int)
        }
    
    def run(self, inputs):
        # Custom synthesis logic
        results = []
        for input_data in inputs:
            # Apply your custom rules here
            synthesized = self._synthesize_financial_row(input_data)
            results.append(synthesized)
        return results
    
    def _synthesize_financial_row(self, row_data):
        # Custom synthesis implementation
        # This is where you'd add your domain logic
        return modified_data

# Usage in DreamBolt
synthesizer = DataSynthesizer()
with DataDreamer("Custom Financial Pipeline"):
    custom_step = CustomFinancialSynthesis("financial_synth")
    result = custom_step.run([input_data])
```

## Integration with DreamBolt Pipeline

To integrate custom steps with DreamBolt's main pipeline, modify the `synth.py` file:

```python
# In synth.py, add to DataSynthesizer class:
def synthesize_with_custom_step(self, df: pd.DataFrame, custom_step_class, **kwargs):
    """Synthesize using a custom DataDreamer step."""
    
    with DataDreamer("DreamBolt Custom Synthesis"):
        # Convert DataFrame to DataDreamer format
        input_step = self._df_to_datadreamer_input(df)
        
        # Apply custom step
        custom_step = custom_step_class("custom_synthesis", **kwargs)
        custom_result = custom_step.run(input_step)
        
        # Convert back to DataFrame
        result_df = self._datadreamer_to_df(custom_result)
        
        return result_df
```

## Advanced Examples

### Domain-Specific Validation

```python
class HealthcareDataValidator(Step):
    """Validate healthcare data synthesis."""
    
    def setup(self):
        self.valid_conditions = [
            'Diabetes', 'Hypertension', 'Asthma', 'Depression'
        ]
        self.age_ranges = {
            'child': (0, 12),
            'teen': (13, 17), 
            'adult': (18, 64),
            'senior': (65, 120)
        }
    
    def run(self, inputs):
        validated_results = []
        for row in inputs:
            if self._validate_healthcare_row(row):
                validated_results.append(row)
            else:
                # Re-synthesize or skip invalid rows
                corrected_row = self._correct_healthcare_row(row)
                validated_results.append(corrected_row)
        return validated_results
    
    def _validate_healthcare_row(self, row):
        # Custom validation logic
        age = row.get('age', 0)
        condition = row.get('condition', '')
        
        # Age must be reasonable
        if not (0 <= age <= 120):
            return False
            
        # Condition must be in valid list
        if condition not in self.valid_conditions:
            return False
            
        return True
```

### API Integration Step

```python
class ExternalAPIEnrichment(Step):
    """Enrich data using external APIs."""
    
    def setup(self):
        import requests
        self.session = requests.Session()
        self.api_key = os.getenv('EXTERNAL_API_KEY')
    
    def run(self, inputs):
        enriched_results = []
        for row in inputs:
            # Call external API
            enriched_data = self._call_enrichment_api(row)
            enriched_results.append(enriched_data)
        return enriched_results
    
    def _call_enrichment_api(self, row_data):
        # Make API call and merge results
        response = self.session.get(
            f"https://api.example.com/enrich",
            params={'data': row_data},
            headers={'Authorization': f'Bearer {self.api_key}'}
        )
        
        if response.status_code == 200:
            api_data = response.json()
            return {**row_data, **api_data}
        else:
            return row_data  # Return original if API fails
```

## CLI Integration

You can integrate custom steps with the DreamBolt CLI by adding them to the synthesis options:

```python
# In cli.py, modify the ingest command:
@app.command("ingest")
def ingest_data(
    # ... existing parameters ...
    custom_step: Optional[str] = typer.Option(
        None,
        "--custom-step",
        help="Custom DataDreamer step to apply"
    )
):
    # ... existing code ...
    
    if custom_step:
        # Load and apply custom step
        step_class = load_custom_step(custom_step)
        final_df = synthesizer.synthesize_with_custom_step(
            cleaned_df, step_class
        )
```

## Best Practices

### 1. Error Handling
```python
def run(self, inputs):
    results = []
    for input_data in inputs:
        try:
            result = self._process_input(input_data)
            results.append(result)
        except Exception as e:
            logger.error(f"Failed to process input: {e}")
            # Decide whether to skip or use fallback
            results.append(input_data)  # Fallback to original
    return results
```

### 2. Configuration Management
```python
class ConfigurableStep(Step):
    def __init__(self, config_path: str = None, **kwargs):
        super().__init__(**kwargs)
        self.config = self._load_config(config_path)
    
    def _load_config(self, config_path):
        if config_path and Path(config_path).exists():
            with open(config_path) as f:
                return json.load(f)
        return self._default_config()
```

### 3. Testing Custom Steps
```python
# tests/test_custom_steps.py
def test_custom_financial_step():
    """Test custom financial synthesis step."""
    step = CustomFinancialSynthesis("test_step")
    step.setup()
    
    test_input = [{'revenue': 100000, 'employees': 10}]
    result = step.run(test_input)
    
    assert len(result) == 1
    assert result[0]['revenue'] > 0
    assert 0.05 <= result[0]['profit_margin'] <= 0.25
```

## Contributing Custom Steps

1. Create your custom step following the patterns above
2. Add comprehensive tests in `tests/test_custom_steps.py`
3. Update this documentation with your example
4. Submit a PR with the `feat: custom-step` label

## Resources

- [DataDreamer Documentation](https://datadreamer.dev/)
- [DreamBolt Architecture](../README.md#api-reference)
- [Example Custom Steps](./examples/) 