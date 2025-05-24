import os, time
from argparse import ArgumentParser
from pathlib import Path
from classes.config import Config

from helper.extractor import extract_text_custom
from helper.creator import create_window_page, merge_pdfs
from helper.config import load_config
from helper.check_address_fr import check_address, address_integrity_check, manual_edit

CONFIG: Config
REGEX: str

def main():
    start = time.time()
    global CONFIG
    parser = ArgumentParser(description="Extract text from a PDF file.")
    parser.add_argument("pdf_path", type=Path, help="The path to the PDF file.")
    parser.add_argument("config_path", type=Path, help="The path to the configuration file.")
    args = parser.parse_args()

    CONFIG, REGEX = load_config(args.config_path)  # type: ignore[reportConstant]

    print(
        f"Extracting text from {args.pdf_path} using {CONFIG.extraction_type.name} extraction type."
    )
    print("==========================")
    r = None
    for skip in range(6):
        r = extract_text_custom(args.pdf_path, CONFIG.extraction_type, skip, CONFIG.search_string)
        # Check if address is found:
        if CONFIG.use_regex:
            if address_integrity_check(REGEX, r):
                print(f"Address found with index {skip}.")
                break
        else:
            break
    if r is None:
        print("No address found in the PDF. Please refine your settings in your config file.")
        return
    print(r)
    if 'France' in r:
        print("==========================")
        print('Applying rectification to the address')
        r = check_address(r)
        print('===========================')
        print('CORRECTED ADDRESS:\n{}'.format(r))
        print("==========================")
    else:
        print('Skipping address check (NOT_IN_FRANCE)')
        r = manual_edit(r)

    # create pdf
    output_path = args.pdf_path.with_name(args.pdf_path.stem + "_window.pdf")
    if isinstance(r, list):
        r = "\n".join(r)
    create_window_page(r, str(output_path), CONFIG)

    print("Merging PDF files.")
    merge_pdfs(
        str(args.pdf_path),
        str(output_path),
        str(args.pdf_path.with_name(args.pdf_path.stem + "_merged.pdf")),
    )
    print("Deleting temporary window PDF file.")
    os.remove(output_path)
    print("Completed in {:.2f} seconds.".format(time.time() - start))


if __name__ == "__main__":
    main()
