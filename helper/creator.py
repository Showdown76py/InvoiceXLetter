"""
Helper module to create a DL-envelope window page and merge PDFs.
"""

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PyPDF2 import PdfReader, PdfWriter

from classes.config import FontConfig

_MM_TO_PT = 2.83465  # 1 mm = 2.83465 pt
# A4 page size (mm)
_PAGE_WIDTH_MM = 210
_PAGE_HEIGHT_MM = 297
# Envelope window size (mm)
_WINDOW_WIDTH_MM = 100
_WINDOW_HEIGHT_MM = 50
_MARGIN_RIGHT_MM = 20  # Margin to right edge (mm)
_MARGIN_TOP_MM = 50  # Margin to top edge (mm)

# Compute window origin (lower-left) and top in mm
_WINDOW_X_MM = _PAGE_WIDTH_MM - _MARGIN_RIGHT_MM - _WINDOW_WIDTH_MM
_WINDOW_Y_TOP_MM = _PAGE_HEIGHT_MM - _MARGIN_TOP_MM


def create_window_page(
    text: str,
    output_path: str,
    show_window_border: bool,
    font: FontConfig | None = None,
) -> None:
    """
    Create an A4 PDF page with given text placed at the envelope window position,
    right-aligned with specified margins.

    Args:
        text (str): The multi-line text to print in the window.
        output_path (str): Path to the generated PDF file.
        font (FontConfig | None): Font configuration for the text. If None, default font is used.
    """
    # Convert window origin and top to points
    x0_pt = _WINDOW_X_MM * _MM_TO_PT
    y_top_pt = _WINDOW_Y_TOP_MM * _MM_TO_PT

    c = canvas.Canvas(output_path, pagesize=A4)
    # Register and use custom font if font.path is provided
    if font and font.path:
        # Register the font with a unique name (use font.name)
        print("Using custom font:", font.name, "from path:", font.path)
        pdfmetrics.registerFont(TTFont(font.name, font.path))
        c.setFont(font.name, font.size)
    elif font:
        print("Using installed font:", font.name)
        c.setFont(font.name, font.size)
    else:
        print("Using default font: Helvetica")
        c.setFont("Helvetica", 12)  # Default font
    line_height = 14  # Approximate line height in points for Helvetica 12

    lines = text.splitlines()
    for i, line in enumerate(lines):
        # Compute Y position for each line (downwards from window top)
        current_y = y_top_pt - (i * line_height)
        # Left-align text within window
        c.drawString(x0_pt, current_y, line)

    # Dessiner le contour de la fenêtre si demandé
    if show_window_border:
        window_x_pt = _WINDOW_X_MM * _MM_TO_PT
        window_w_pt = _WINDOW_WIDTH_MM * _MM_TO_PT
        text_height_pt = len(lines) * line_height
        window_y_pt = (_WINDOW_Y_TOP_MM * _MM_TO_PT) - text_height_pt
        window_h_pt = text_height_pt
        c.saveState()
        c.setStrokeColorRGB(0.8, 0.8, 0.8)  # gris clair
        c.setLineWidth(0.7)
        c.rect(window_x_pt, window_y_pt, window_w_pt, window_h_pt, stroke=1, fill=0)
        c.restoreState()

    c.showPage()
    c.save()


def merge_pdfs(pdf1_path: str, pdf2_path: str, output_path: str) -> None:
    """
    Merge two PDF files into one, concatenating pdf1 then pdf2.

    Args:
        pdf1_path (str): Path to the first PDF.
        pdf2_path (str): Path to the second PDF.
        output_path (str): Path to the merged PDF file.
    """
    writer = PdfWriter()
    # Append pages from first PDF
    reader1 = PdfReader(pdf1_path)
    for page in reader1.pages:
        writer.add_page(page)
    # Append pages from second PDF
    reader2 = PdfReader(pdf2_path)
    for page in reader2.pages:
        writer.add_page(page)
    # Write out
    with open(output_path, "wb") as out_f:
        writer.write(out_f)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Create a DL window page or merge two PDFs."
    )
    sub = parser.add_subparsers(dest="command")
    # Sub-command: create
    p_create = sub.add_parser("create", help="Generate window page with text.")
    p_create.add_argument("text", type=str, help="Text to place inside the window.")

    p_create.add_argument("output", type=str, help="Output PDF path.")
    # Sub-command: merge
    p_merge = sub.add_parser("merge", help="Merge two PDFs.")
    p_merge.add_argument("pdf1", type=str, help="First PDF path.")
    p_merge.add_argument("pdf2", type=str, help="Second PDF path.")
    p_merge.add_argument("output", type=str, help="Merged PDF output path.")
    args = parser.parse_args()
    if args.command == "create":
        create_window_page(args.text, args.output, False, None)
    elif args.command == "merge":
        merge_pdfs(args.pdf1, args.pdf2, args.output)
    else:
        parser.print_help()
