import hashlib
import uuid
import datetime
from dataclasses import dataclass, field


@dataclass
class Paper:
    """Domain model representing an ingested research paper."""

    raw_text: str
    source_type: str          # "text" | "pdf"
    title: str = ""
    paper_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    text_hash: str = field(default="")
    timestamp: str = field(
        default_factory=lambda: datetime.datetime.utcnow().isoformat()
    )

    def __post_init__(self):
        if not self.text_hash:
            self.text_hash = hashlib.sha256(self.raw_text.encode()).hexdigest()

    def to_dict(self) -> dict:
        return {
            "paper_id": self.paper_id,
            "title": self.title,
            "source_type": self.source_type,
            "text_hash": self.text_hash,
            "timestamp": self.timestamp,
        }
