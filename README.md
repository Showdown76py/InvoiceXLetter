# InvoiceXLetter
InvoiceXLetter is a Python script that adds a page on your PDF invoice to include the address of the recipient, which is useful for enveloppes with a window.
Only DL enveloppes are supported yet.

## Features
Reads the first page of a PDF invoice, extracts the recipient's address, and appends it as a new page at the end of the PDF. The new page is formatted to fit an envelope window, with customizable font and layout options.  
Additional features include:
- **Automatic address verification (in France)** using La Poste's API (Okapi).
- **Support for multiple invoice formats.**
- **Manual address editing** if the automatic extraction has some kind of failure.
- **Use a different config file** depending on the invoice type/envelope you will be using.

## Requirements
- Python 3.6 or higher
- reportlab
- requests
- pdfminer.six

## Installation
You can install the required packages using pip:
```bash
pip install -r requirements.txt
```

## Usage
1. Clone the repository:
```bash
git clone https://github.com/Showdown76py/InvoiceXLetter.git
cd InvoiceXLetter
```
2. Run the script:
```bash
python invoiceXLetter.py <input_pdf>
```
3. The output PDF will be saved as `<name>-output.pdf` in the same directory.
4. Open the output PDF to see the added page with the recipient's address. Make sure to print double-sided to have the address on the back of the invoice.

### License
This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.
