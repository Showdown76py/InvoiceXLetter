from dataclasses import dataclass
from helper.extractor import ExtractionType


@dataclass
class FontConfig:
    name: str
    size: int
    color: str
    path: str | None = None  # Optional path for custom fonts


@dataclass
class Display:
    margin_top: int
    margin_right: int
    width: int
    height: int


@dataclass
class Config:
    extraction_type: ExtractionType
    search_string: str
    use_regex: bool
    show_window_border: bool
    font: FontConfig
    display: Display
