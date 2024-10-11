import os
import pytesseract
from pathlib import Path
from pdf2image import convert_from_path
from typing import Optional

def setup_environment() -> str:
    """Set up the environment for OCR processing."""
    os.environ["TESSDATA_PREFIX"] = r"C:\Program Files\Tesseract-OCR\tessdata"
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    
    poppler_path = r"C:\Program Files\poppler\Library\bin"
    os.environ["PATH"] += os.pathsep + poppler_path
    return poppler_path

def extract_text_from_pdf(pdf_path: str, output_file: Optional[str] = None, language: str = 'ben') -> str:
    """
    Extract text from a PDF file using OCR.

    Args:
        pdf_path (str): Path to the input PDF file.
        output_file (Optional[str]): Path to save the extracted text. If None, uses the PDF filename.
        language (str): Language for OCR. Default is 'ben' (Bengali).

    Returns:
        str: The extracted text from the PDF.
    """
    poppler_path = setup_environment()
    
    pdf_path = Path(pdf_path)
    if not output_file:
        output_file = pdf_path.with_suffix('.txt')
    else:
        output_file = Path(output_file)

    full_book = ""
    
    images = convert_from_path(pdf_path, poppler_path=poppler_path)

    for i, image in enumerate(images, start=1):
        text = pytesseract.image_to_string(image, lang=language)
        full_book += f"\n--- Page {i} ---\n{text}"
        print(f"Page {i} processed.")

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(full_book)

    print(f"Text extracted and saved to {output_file}")
    return full_book

def process_pdf(pdf_path: str, output_file: Optional[str] = None, language: str = 'ben') -> str:
    """
    Process a PDF file and extract text.

    This function is the main entry point for external use.

    Args:
        pdf_path (str): Path to the input PDF file.
        output_file (Optional[str]): Path to save the extracted text. If None, uses the PDF filename.
        language (str): Language for OCR. Default is 'ben' (Bengali).

    Returns:
        str: The extracted text from the PDF.
    """
    extracted_text = extract_text_from_pdf(pdf_path, output_file, language)
    print(f"Extraction complete. Text length: {len(extracted_text)} characters")
    return extracted_text

if __name__ == "__main__":
    # Example
    pdf_file = r"Freedom Fight.pdf"
    process_pdf(pdf_file)
