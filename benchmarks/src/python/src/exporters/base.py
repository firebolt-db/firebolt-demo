from abc import ABC, abstractmethod
from typing import Dict, Any

class BenchmarkExporter(ABC):
    @abstractmethod
    def export(self, results: Dict[str, Any], output_dir: str) -> None:
        """Export benchmark results"""
        pass
