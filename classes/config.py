import dataclasses
from helper.extractor import ExtractionType

@dataclasses.dataclass
class FontConfig:
    name: str
    size: int
    color: str
    path: str | None = None # Optional path for custom fonts

@dataclasses.dataclass
class Config:
    extraction_type: ExtractionType
    search_string: str
    show_window_border: bool
    font: FontConfig
