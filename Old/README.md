# PDF OCR Text Extractor for Bengali

[![Bangla RAG](https://img.shields.io/badge/Bangla%20RAG-Visit%20Project-blue)](https://github.com/Bangla-RAG/PoRAG)
[![Tesseract OCR](https://img.shields.io/badge/Tesseract%20OCR-Download-green)](https://github.com/UB-Mannheim/tesseract/wiki)
[![Poppler](https://img.shields.io/badge/Poppler-Download-orange)](https://github.com/oschwartz10612/poppler-windows/releases/download/v24.08.0-0/Release-24.08.0-0.zip)

This Python script is part of the Bangla RAG (Retrieval-Augmented Generation) pipeline project, specifically designed to enhance the PoRAG (https://github.com/Bangla-RAG/PoRAG) system. It extracts Bengali text from PDF files using Optical Character Recognition (OCR). This functionality is particularly useful for incorporating scanned or non-searchable PDFs containing Bengali text into the RAG pipeline, thereby improving the system's ability to process and generate responses based on a wider range of Bangla language resources.

## Features

- Extract Bengali text from PDFs using OCR (default language)
- Support for other languages through optional parameters
- Automatic output file naming
- Progress bar for tracking OCR process
- Configurable via environment variables
- Command-line interface for easy usage
- Multithreading for faster processing

## Prerequisites

1. **Python 3.6+**

2. **Tesseract OCR**:
   - Download from: https://github.com/UB-Mannheim/tesseract/wiki
   - Ensure Bengali language data is installed

3. **Poppler**:
   - For Windows:
     - Download from: https://github.com/oschwartz10612/poppler-windows/releases/download/v24.08.0-0/Release-24.08.0-0.zip
     - Extract the ZIP file to one of the following common directories:
       - `C:\Program Files`
       - `C:\Program Files (x86)`
       - Your user's Downloads folder
     - Add the `bin` directory of the extracted Poppler folder to your system's PATH
   - For Unix-based systems (Linux, macOS):
     - Use your package manager to install Poppler. For example:
       - Ubuntu/Debian: `sudo apt-get install poppler-utils`
       - macOS (using Homebrew): `brew install poppler`
     - Poppler should be automatically available in common directories like `/usr/bin` or `/usr/local/bin`

   Note: The script will automatically search for Poppler in these common directories. If you install Poppler in a different location, you may need to set the `POPPLER_PATH` environment variable.

4. **Python Libraries**:
   Install the required Python packages using the provided `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```

## Installation

1. Clone this repository or download `ocr.py` and `requirements.txt`.
2. Set up all prerequisites as described above, ensuring Tesseract OCR and Poppler are properly installed on your system.
3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Ensure that both Tesseract and Poppler executables are in your system's PATH or set the appropriate environment variables (TESSERACT_PATH and POPPLER_PATH).

## Configuration

You can configure the script using environment variables:

- `TESSERACT_PATH`: Path to the Tesseract executable
- `POPPLER_PATH`: Path to the Poppler bin directory
- `OCR_LANGUAGE`: Default language for OCR (default is 'ben' for Bengali)

If these are not set, the script will attempt to find the required executables automatically.

## Usage

### As a script:

```
python ocr.py [pdf_path] [-o OUTPUT] [-l LANGUAGE]
```

- `pdf_path`: Path to the input PDF file (default: "Freedom Fight.pdf")
- `-o` or `--output`: Path to save the extracted text (optional)
- `-l` or `--language`: Language for OCR (default: 'ben' for Bengali)

Examples:
```
# Process a Bengali PDF (default)
python ocr.py "my_bengali_document.pdf"

# Process an English PDF
python ocr.py "english_document.pdf" -l eng

# Specify output file
python ocr.py "document.pdf" -o "output.txt"
```

If no arguments are provided, it will process "Freedom Fight.pdf" with Bengali as the default language.

### As a module:

```
from ocr import process_pdf

# Process a Bengali PDF (default)
extracted_text = process_pdf("path/to/your/bengali_document.pdf")

# Process an English PDF
english_text = process_pdf("path/to/english_document.pdf", language="eng")

print(extracted_text)
```

## How it works

1. **Environment Setup**: The script first checks for environment variables or attempts to find Tesseract and Poppler automatically.

2. **PDF to Image Conversion**: The PDF is converted to images using Poppler.

3. **OCR Processing**: Each image is processed using Tesseract OCR with multithreading for improved performance. Bengali is used as the default language unless specified otherwise.

4. **Text Compilation**: The extracted text from all pages is compiled in the correct order.

## Limitations

- OCR accuracy depends on PDF quality and text complexity
- Large PDFs may take significant processing time
- Complex layouts might not be processed accurately

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to open an issue or submit a pull request.

## Acknowledgments
- Tesseract OCR: https://github.com/tesseract-ocr/tesseract
- Poppler: https://poppler.freedesktop.org/
- tqdm: https://github.com/tqdm/tqdm
- argparse: https://docs.python.org/3/library/argparse.html
- https://github.com/shihabshahid/python_bangla_ocr_pdf_to_text
- https://github.com/pritomshad/bangla-pdf-to-text-OCR