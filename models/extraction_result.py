import uuid
import datetime
from dataclasses import dataclass, field
from typing import List


@dataclass
class ExtractionResult:
    """Domain model for structured elements extracted from a paper."""

    paper_id: str
    datasets: List[str]
    methods: List[str]
    citations: List[str]
    model_name: str
    extraction_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = field(
        default_factory=lambda: datetime.datetime.utcnow().isoformat()
    )

    def to_dict(self) -> dict:
        return {
            "extraction_id": self.extraction_id,
            "paper_id": self.paper_id,
            "datasets": self.datasets,
            "methods": self.methods,
            "citations": self.citations,
            "model_name": self.model_name,
            "timestamp": self.timestamp,
        }
