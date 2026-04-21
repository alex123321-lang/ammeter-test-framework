from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class TestResult:
    ammeter_type: str
    measurements: List[float]
    statistics: Dict[str, float]
    error: Optional[str] = None

    meta: Dict = None

    @property
    def is_success(self) -> bool:
        return self.error is None