import os
import sys
import subprocess
import logging
from pathlib import Path
from typing import Optional, List
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
from tqdm import tqdm

TESSERACT_PATH = os.environ.get("TESSERACT_PATH")
POPPLER_PATH = os.environ.get("POPPLER_PATH")
DEFAULT_LANGUAGE = os.environ.get("OCR_LANGUAGE", "ben")

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class OCRProcessor:
    """
    A class to process PDF files and extract text using OCR.

    This class handles the conversion of PDF to images and the OCR processing
    of those images to extract text.
    """

    def __init__(self, language: str = DEFAULT_LANGUAGE):
        """
        Initialize the OCRProcessor.

        Args:
            language (str): The language to use for OCR. Defaults to Bengali.
        """
        self.language = language
        self.tesseract_path = TESSERACT_PATH or self.find_tesseract()
        self.poppler_path = POPPLER_PATH or self.find_poppler()
        logging.info(f"Tesseract path: {self.tesseract_path}")
        logging.info(f"Poppler path: {self.poppler_path}")

    @staticmethod
    def find_program(program: str) -> Optional[str]:
        """
        Find the path to a program.

        Args:
            program (str): The name of the program to find.

        Returns:
            Optional[str]: The path to the program if found, None otherwise.
        """
        logging.info(f"Searching for {program}")
        if sys.platform.startswith("win"):
            program += ".exe"

        # Check in PATH
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = Path(path) / program
            if exe_file.is_file() and os.access(str(exe_file), os.X_OK):
                logging.info(f"Found {program} in PATH: {exe_file}")
                return str(exe_file)

        # Search in common installation directories
        common_dirs = [
            Path(os.environ.get("ProgramFiles", "C:/Program Files")),
            Path(os.environ.get("ProgramFiles(x86)", "C:/Program Files (x86)")),
            Path(os.environ.get("USERPROFILE", "~")) / "Downloads",
            Path("/usr/bin"),
            Path("/usr/local/bin"),
            Path("/opt"),
            Path.home() / "Downloads",
        ]

        for directory in common_dirs:
            for exe_file in directory.rglob(program):
                if exe_file.is_file() and os.access(str(exe_file), os.X_OK):
                    logging.info(f"Found {program} in common directory: {exe_file}")
                    return str(exe_file)

        logging.warning(f"{program} not found")
        return None

    def find_tesseract(self) -> str:
        """
        Find the Tesseract executable.

        Returns:
            str: The path to the Tesseract executable.

        Raises:
            EnvironmentError: If Tesseract is not found.
        """
        tesseract = self.find_program("tesseract")
        if not tesseract:
            raise EnvironmentError(
                "Tesseract not found. Please install it and make sure it's in your PATH."
            )
        return tesseract

    def find_poppler(self) -> str:
        """
        Find the Poppler (pdftoppm) executable.

        Returns:
            str: The path to the Poppler directory.

        Raises:
            EnvironmentError: If Poppler (pdftoppm) is not found.
        """
        pdftoppm = self.find_program("pdftoppm")
        if not pdftoppm:
            raise EnvironmentError(
                "Poppler (pdftoppm) not found. Please install it and make sure it's in your PATH."
            )
        return str(Path(pdftoppm).parent)

    def convert_pdf_to_images(self, pdf_path: Path) -> List[Path]:
        """
        Convert PDF to images.

        Args:
            pdf_path (Path): The path to the PDF file.

        Returns:
            List[Path]: A list of paths to the generated image files.

        Raises:
            subprocess.CalledProcessError: If the conversion fails.
        """
        image_prefix = f"temp_image_{os.getpid()}"
        pdftoppm_path = os.path.join(self.poppler_path, "pdftoppm")
        logging.info(f"Converting PDF to images using {pdftoppm_path}")
        try:
            subprocess.run(
                [pdftoppm_path, "-png", str(pdf_path), image_prefix],
                check=True,
                capture_output=True,
                text=True,
            )
        except subprocess.CalledProcessError as e:
            logging.error(f"Error converting PDF to images: {e}")
            logging.error(f"pdftoppm stderr: {e.stderr}")
            raise
        return sorted(Path().glob(f"{image_prefix}-*.png"))

    def process_image(self, image_file: Path, page_num: int) -> str:
        """
        Process a single image with OCR.

        Args:
            image_file (Path): The path to the image file.
            page_num (int): The page number of the image.

        Returns:
            str: The extracted text from the image.
        """
        try:
            logging.info(f"Processing page {page_num}")
            result = subprocess.run(
                [self.tesseract_path, str(image_file), "stdout", "-l", self.language],
                capture_output=True,
                check=True,
                encoding="utf-8",
            )
            text = result.stdout
            os.remove(image_file)  # Clean up temporary image file
            return f"\n--- Page {page_num} ---\n{text}"
        except subprocess.CalledProcessError as e:
            logging.error(f"Error processing page {page_num}: {e}")
            logging.error(f"Tesseract stderr: {e.stderr}")
            return f"\n--- Page {page_num} ---\nError: {e}\n"

    def extract_text_from_pdf(
        self, pdf_path: str, output_file: Optional[str] = None
    ) -> str:
        """
        Extract text from a PDF file using OCR.

        Args:
            pdf_path (str): The path to the PDF file.
            output_file (Optional[str]): The path to save the extracted text.

        Returns:
            str: The extracted text from the PDF.
        """
        pdf_path = Path(pdf_path)
        if not output_file:
            output_file = pdf_path.with_suffix(".txt")
        else:
            output_file = Path(output_file)

        logging.info(f"Extracting text from {pdf_path}")
        images = self.convert_pdf_to_images(pdf_path)
        full_book = [""] * len(images)

        with ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(self.process_image, img, i): i
                for i, img in enumerate(images, start=1)
            }
            for future in tqdm(
                as_completed(futures), total=len(futures), desc="Processing pages"
            ):
                page_num = futures[future]
                try:
                    page_text = future.result()
                    full_book[page_num - 1] = page_text
                except Exception as exc:
                    logging.error(
                        f"Page {page_num} processing generated an exception: {exc}"
                    )
                    full_book[page_num - 1] = (
                        f"\n--- Page {page_num} ---\nError: {exc}\n"
                    )

        full_text = "".join(full_book)

        with open(output_file, "w", encoding="utf-8") as file:
            file.write(full_text)

        logging.info(f"Text extracted and saved to {output_file}")
        return full_text


def process_pdf(
    pdf_path: str, output_file: Optional[str] = None, language: str = "ben"
) -> str:
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
    processor = OCRProcessor(language)
    extracted_text = processor.extract_text_from_pdf(pdf_path, output_file)
    logging.info(f"Extraction complete. Text length: {len(extracted_text)} characters")
    return extracted_text


def main():
    """Main function to handle command-line usage."""
    parser = argparse.ArgumentParser(description="Extract text from PDF using OCR")
    parser.add_argument(
        "pdf_path",
        nargs="?",
        default="Freedom Fight.pdf",
        help="Path to the input PDF file",
    )
    parser.add_argument("-o", "--output", help="Path to save the extracted text")
    parser.add_argument(
        "-l", "--language", default="ben", help="Language for OCR (default: ben)"
    )

    args, _ = parser.parse_known_args()

    try:
        extracted_text = process_pdf(args.pdf_path, args.output, args.language)
        print(f"Extraction completed successfully. Processed file: {args.pdf_path}")
    except Exception as e:
        logging.error(f"An error occurred during extraction: {e}")
        print(f"An error occurred. Please check the log for details.")


if __name__ == "__main__":
    main()
