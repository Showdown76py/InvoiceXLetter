"""
This module provides functions to extract text from PDF files.
"""

import io
import enum

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBox


class ExtractionType(enum.Enum):
    CONTAINS = "contains"  # Get the text that contains the given string
    FOLLOWING = "following"  # Get the text that follows the given string
    PRECEDING = "preceding"  # Get the text that precedes the given string


def extract_text_custom(
    pdf_path: str, extraction_type: ExtractionType, skip: int, search_string: str
) -> str:
    """
    Extracts text from a PDF file according to the extraction type and search string.

    Args:
        pdf_path (str): The path to the PDF file.
        extraction_type (ExtractionType): The type of extraction to perform.
        search_string (str): The string to search for in the PDF file.
    Returns:
        str: The extracted text.
    """
    output = io.StringIO()
    try:
        for page_layout in extract_pages(pdf_path):
            # Collect all textboxes as objects and as text
            textboxes = [
                element for element in page_layout if isinstance(element, LTTextBox)
            ]
            textbox_texts: list[str] = []
            for tb in textboxes:
                lines = [
                    text_line.get_text().strip()
                    for text_line in tb
                ]
                textbox_texts.append("\n".join([line for line in lines if line]))

            result: list[str] = []
            for idx, tb_text in enumerate(textbox_texts):
                if extraction_type == ExtractionType.CONTAINS:
                    if search_string in tb_text:
                        result.append(f"{tb_text}")
                elif extraction_type == ExtractionType.FOLLOWING:
                    if search_string in tb_text and idx + 1 + skip < len(textbox_texts):
                        following = textbox_texts[idx + 1 + skip]
                        result.append(f"{following}")
                elif extraction_type == ExtractionType.PRECEDING:
                    if search_string in tb_text and idx - 1 - skip >= 0:
                        preceding = textbox_texts[idx - 1 - skip]
                        result.append(f"{preceding}")
            output.write("".join(result))
        return output.getvalue()
    except Exception as e:
        return f"Error: {e}"
