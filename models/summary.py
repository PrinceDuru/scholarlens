import uuid
import datetime
from dataclasses import dataclass, field
from typing import List


@dataclass
class Summary:
    """Domain model representing an LLM-generated paper summary."""

    paper_id: str
    summary_text: str
    contributions: List[str]
    model_name: str
    summary_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = field(
        default_factory=lambda: datetime.datetime.utcnow().isoformat()
    )

    def to_dict(self) -> dict:
        return {
            "summary_id": self.summary_id,
            "paper_id": self.paper_id,
            "summary_text": self.summary_text,
            "contributions": self.contributions,
            "model_name": self.model_name,
            "timestamp": self.timestamp,
        }
