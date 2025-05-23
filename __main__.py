import json, os
from argparse import ArgumentParser
from pathlib import Path
from classes.config import Config, FontConfig

from helper.extractor import extract_text_custom, ExtractionType
from helper.creator import create_window_page, merge_pdfs
CONFIG: Config


def load_config():
    with open("config.json", "r") as f:
        config_data = json.load(f)
    return Config(
        extraction_type=ExtractionType(config_data["extraction_type"]),
        search_string=config_data["search_string"],
        show_window_border=config_data["show_window_border"],
        font=FontConfig(
            name=config_data["font"]["name"],
            size=config_data["font"]["size"],
            color=config_data["font"]["color"],
            path=config_data["font"].get("path")  # Optional path for custom fonts
        )
    )

def main():
    global CONFIG;CONFIG=load_config()
    parser = ArgumentParser(description="Extract text from a PDF file.")
    parser.add_argument("pdf_path", type=Path, help="The path to the PDF file.")
    args = parser.parse_args()

    print(f'Extracting text from {args.pdf_path} using {CONFIG.extraction_type.name} extraction type.')
    print('==========================')
    r = extract_text_custom(args.pdf_path, CONFIG.extraction_type, CONFIG.search_string)
    print(r)
    print('==========================')

    # create pdf
    output_path = args.pdf_path.with_name(args.pdf_path.stem + "_window.pdf")
    create_window_page(r, str(output_path), CONFIG.show_window_border, CONFIG.font)

    print('Merging PDF files.')
    merge_pdfs(
        str(args.pdf_path),
        str(output_path),
        str(args.pdf_path.with_name(args.pdf_path.stem + "_merged.pdf"))
    )
    print('Deleting temporary window PDF file.')
    os.remove(output_path)
    print('Done!')

if __name__ == "__main__":
    main()
