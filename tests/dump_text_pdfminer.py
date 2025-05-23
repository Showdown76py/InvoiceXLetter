"""
This tool dumps the text from each text box in a PDF file to a text file using pdfminer.six.
"""
import sys
import argparse
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBox, LTTextLine

def dump_textboxes_from_pdf(pdf_path: str, output_path: str) -> None:
    """
    Dumps the text from each text box in a PDF file to a text file.

    Args:
        pdf_path (str): The path to the PDF file.
        output_path (str): The path to the output text file.
    """
    try:
        with open(output_path, "w", encoding="utf-8") as text_file:
            for page_num, page_layout in enumerate(extract_pages(pdf_path)):
                text_file.write(f"------ Page {page_num + 1} ------\n")
                for element in page_layout:
                    if isinstance(element, LTTextBox):
                        text_file.write("[TextBox]\n")
                        for text_line in element:
                            if isinstance(text_line, LTTextLine):
                                text = text_line.get_text().strip()
                                if text:
                                    text_file.write(text + "\n")
                        text_file.write("\n")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Dump text boxes from a PDF file to a text file using pdfminer.six.")
    parser.add_argument("pdf_path", type=str, help="The path to the PDF file.")
    parser.add_argument("output_path", type=str, help="The path to the output text file.")
    args = parser.parse_args()

    dump_textboxes_from_pdf(args.pdf_path, args.output_path)

if __name__ == "__main__":
    main()
