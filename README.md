# Bangla PDF OCR

[![PyPI version](https://badge.fury.io/py/bangla-pdf-ocr.svg)](https://badge.fury.io/py/bangla-pdf-ocr)
[![Bangla RAG](https://img.shields.io/badge/Bangla%20RAG-Visit%20Project-blue)](https://github.com/Bangla-RAG/PoRAG)

> **Note:** This repository is the official home for the `bangla-pdf-ocr` package. You can use this repository for package-related issues, discussions, and contributions. We welcome your feedback and involvement in improving the tool!

Bangla PDF OCR is a powerful tool that extracts Bengali text from PDF files. It's designed for simplicity and works on Windows, macOS, and Linux without any extra downloads or configurations. This tool was initially developed as a part of the Bangla RAG (Retrieval-Augmented Generation) pipeline project, specifically designed to enhance the [PoRAG](https://github.com/Bangla-RAG/PoRAG) system, but it can be used independently for Bengali OCR tasks. Use it as a standalone tool for your Bengali OCR needs.



## Key Features

- Extracts Bengali text from PDFs quickly and accurately
- Works on Windows, macOS, and Linux
- Easy to use from both command line and Python scripts
- Installs all necessary components automatically
- Supports other languages besides Bengali
- Multi-threaded processing for improved performance

## Quick Start

1. Install the package:
   ```bash
   pip install bangla-pdf-ocr
   ```

2. Run the setup command to install dependencies:
   ```bash
   bangla-pdf-ocr-setup
   ```

3. Start using it right away!

   From command line:
   ```bash
   bangla-pdf-ocr your_file.pdf
   ```

   In your Python script:
   ```python
   from bangla_pdf_ocr import process_pdf
   path = "path/to/your/pdf_file.pdf"
   output_file = "output.txt"
   extracted_text = process_pdf(path, output_file)
   print(extracted_text)
   ```

That's it! No additional downloads or configurations needed.

## Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

## Installation

1. Install the package from PyPI:
   ```bash
   pip install bangla-pdf-ocr
   ```

2. Set up system dependencies:
   ```bash
   bangla-pdf-ocr-setup
   ```
   This command installs necessary dependencies based on your operating system:
   - Linux: Installs `tesseract-ocr`, `poppler-utils`, and `tesseract-ocr-ben`
   - macOS: Installs `tesseract`, `poppler`, and `tesseract-lang` via Homebrew
   - Windows: Downloads and installs Tesseract OCR and Poppler, adding them to the system PATH

   Note: On Windows, you may need to run the command prompt as administrator.

3. Verify the installation:
   ```bash
   bangla-pdf-ocr-verify
   ```
   This command checks if all required dependencies are properly installed and accessible.

## Usage

### Command-line Interface

Basic usage:
```bash
bangla-pdf-ocr [input_pdf] [-o output_file] [-l language]
```

### Options:
- `input_pdf`: Path to the input PDF file (optional, uses a sample PDF if not provided)
- `-o, --output`: Specify the output file path (default: input filename with `.txt` extension)
- `-l, --language`: Specify the OCR language (default: 'ben' for Bengali)

### Examples:

1. Process the default sample PDF:
   ```bash
   bangla-pdf-ocr
   ```

2. Process a specific PDF:
   ```bash
   bangla-pdf-ocr path/to/my_document.pdf
   ```

3. Specify an output file:
   ```bash
   bangla-pdf-ocr path/to/my_document.pdf -o path/to/extracted_text.txt
   ```

4. Try a sample PDF extraction:
   ```bash
   bangla-pdf-ocr
   ```
   This command processes a sample Bengali PDF file included with the package, demonstrating the text extraction capabilities.

### Using as a Python Module

You can also use Bangla PDF OCR as a module in your Python scripts:

```python
from bangla_pdf_ocr import process_pdf

path = "bangla_pdf_ocr\data\Freedom Fight.pdf"
output_file = "Extracted_text.txt"
extracted_text = process_pdf(path, output_file)

print(f"Text extracted and saved to: {output_file}")
```

## Troubleshooting

If you encounter any issues:

1. Run the verification command:
   ```bash
   bangla-pdf-ocr-verify
   ```

2. For Windows users:
   - Run `setup/verify` command prompts as administrator if you encounter permission issues.
   - Restart your command prompt or IDE after installation to ensure PATH changes take effect.

3. Check the console output and logs for any error messages.

4. If automatic installation fails, refer to the manual installation instructions provided by the setup command.

5. Ensure you have the latest version of the package:
   ```bash
   pip install --upgrade bangla-pdf-ocr
   ```

6. If problems persist, please open an issue on our GitHub repository with detailed information about the error and your system configuration.

## Reporting Issues

If you encounter any problems or have suggestions for Bangla PDF OCR:

1. Check [existing issues](https://github.com/asiff00/bangla-pdf-ocr/issues) to see if your issue has already been reported.
2. If not, [create a new issue](https://github.com/asiff00/bangla-pdf-ocr/issues/new) on our GitHub repository.
3. Provide detailed information about the problem, including steps to reproduce it.

We appreciate your feedback to help improve Bangla PDF OCR!

## Acknowledgments

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [Poppler](https://poppler.freedesktop.org/)
- [python_bangla_ocr_pdf_to_text](https://github.com/shihabshahid/python_bangla_ocr_pdf_to_text)
- [bangla-pdf-to-text-OCR](https://github.com/pritomshad/bangla-pdf-to-text-OCR)

Happy OCR processing!
