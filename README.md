# PDF OCR Text Extractor for Bengali

[![Bangla RAG](https://img.shields.io/badge/Bangla%20RAG-Visit%20Project-blue)](https://github.com/Bangla-RAG/PoRAG)
[![Tesseract OCR](https://img.shields.io/badge/Tesseract%20OCR-Download-green)](https://github.com/UB-Mannheim/tesseract/wiki)
[![Poppler](https://img.shields.io/badge/Poppler-Download-orange)](https://github.com/oschwartz10612/poppler-windows/releases/download/v24.08.0-0/Release-24.08.0-0.zip)

This Python script is part of the Bangla RAG (Retrieval-Augmented Generation) pipeline project, specifically designed to enhance the PoRAG (https://github.com/Bangla-RAG/PoRAG) system. It extracts Bengali text from both PDF and TXT files, with a focus on Optical Character Recognition (OCR) for PDFs. This functionality is particularly useful for incorporating scanned or non-searchable PDFs containing Bengali text into the RAG pipeline, thereby improving the system's ability to process and generate responses based on a wider range of Bangla language resources.

## Features

- Extract Bengali text from PDFs using OCR
- Automatic output file naming
- Easy to use as a script or imported module

## Prerequisites

1. **Python 3.6+**
2. **Tesseract OCR**:
   - Download from: https://github.com/UB-Mannheim/tesseract/wiki
   - Default path: `C:\Program Files\Tesseract-OCR`
   - Ensure Bengali language data is installed
3. **Poppler**:
   - Download from: https://github.com/oschwartz10612/poppler-windows/releases/download/v24.08.0-0/Release-24.08.0-0.zip
   - Extract the ZIP file
   - By default, the path will be something like: `C:\Users\USER\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin`
   - For better management, you can:
     - Rename the `poppler-24.08.0` folder to simply `poppler`
     - Move this folder to `C:\Program Files\`
   - The final path could be `C:\Program Files\poppler\Library\bin`
   - Ensure this bin directory is added to your system's PATH
4. **Python Libraries**:
   ```bash
   pip install pytesseract pdf2image Pillow
   ```

Ensure Tesseract and Poppler bin directories are in your system's PATH. For Poppler, this means adding `C:\Program Files\poppler\bin` (or `C:\Users\USER\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin`) to your PATH.

## Installation

1. Clone this repository or download `ocr.py`.
2. Set up all prerequisites as described above.
3. If you've used a different path for Poppler, update the `poppler_path` in the `setup_environment()` function:

   ```python
   poppler_path = r"C:\Program Files\poppler\Library\bin"
   # or if you didn't rename the folder:
   # poppler_path = r"C:\Users\USER\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin"
   ```

   Replace `USER` with your Windows username if using the default path.

## Usage

### As a script:
```bash
python ocr.py
```

### As a module:
```python
from ocr import process_pdf

extracted_text = process_pdf("path/to/your/bengali_document.pdf")
print(extracted_text)
```

## How it works

1. **Environment Setup**:
   ```python
   def setup_environment() -> str:
       os.environ["TESSDATA_PREFIX"] = r"C:\Program Files\Tesseract-OCR\tessdata"
       pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
       
       poppler_path = r"C:\Program Files\poppler\Library\bin"
       os.environ["PATH"] += os.pathsep + poppler_path
       return poppler_path
   ```

2. **PDF to Image Conversion** (using Poppler):
   ```python
   images = convert_from_path(pdf_path, poppler_path=poppler_path)
   ```

3. **OCR Processing** (using Tesseract):
   ```python
   for image in images:
       text = pytesseract.image_to_string(image, lang='ben')
       # Process text...
   ```

## Configuration

Modify paths in `setup_environment()` if Tesseract or Poppler are installed in different locations.

## Limitations

- OCR accuracy depends on PDF quality and text complexity
- Large PDFs may take significant processing time
- Complex layouts might not be processed accurately

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to open an issue or submit a pull request.

## Acknowledgments
- https://github.com/UB-Mannheim/tesseract/wiki
- https://github.com/oschwartz10612/poppler-windows/releases/download/v24.08.0-0/Release-24.08.0-0.zip
- https://github.com/shihabshahid/python_bangla_ocr_pdf_to_text
- https://github.com/pritomshad/bangla-pdf-to-text-OCR
