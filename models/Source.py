from dataclasses import dataclass


@dataclass
class Source:
    source_id: int
    source_address: str
    source_status: int
