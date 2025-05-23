"""
This tool dumps the text from a PDF file to a text file.
"""
import sys
import argparse

from PyPDF2 import PdfReader

def dump_text_from_pdf(pdf_path: str, output_path: str) -> None:
    """
    Dumps the text from a PDF file to a text file.

    Args:
        pdf_path (str): The path to the PDF file.
        output_path (str): The path to the output text file.
    """
    try:
        # Open the PDF file
        with open(pdf_path, "rb") as pdf_file:
            reader = PdfReader(pdf_file)
            with open(output_path, "w", encoding="utf-8") as text_file:
                for i, page in enumerate(reader.pages):
                    text_file.write(page.extract_text() + "\n------ Page %d ------\n" % (i + 1))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Dump text from a PDF file to a text file.")
    parser.add_argument("pdf_path", type=str, help="The path to the PDF file.")
    parser.add_argument("output_path", type=str, help="The path to the output text file.")
    args = parser.parse_args()

    dump_text_from_pdf(args.pdf_path, args.output_path)

if __name__ == "__main__":
    main()
