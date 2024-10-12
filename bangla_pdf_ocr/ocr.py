import os
import sys
import subprocess
import logging
from pathlib import Path
from typing import Optional, List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed, Future
import argparse
from tqdm import tqdm
from colorama import init, Fore, Style
import platform
import pkgutil

init(autoreset=True)

TESSERACT_PATH: Optional[str] = os.environ.get("TESSERACT_PATH")
POPPLER_PATH: Optional[str] = os.environ.get("POPPLER_PATH")
DEFAULT_LANGUAGE: str = os.environ.get("OCR_LANGUAGE", "ben")

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger: logging.Logger = logging.getLogger(__name__)


def type_text(text: str, color: str = Fore.WHITE) -> None:
    """Print colored text to the console."""
    print(color + text + Style.RESET_ALL)


class OCRProcessor:
    """
    A class to handle OCR processing of PDF files.

    Attributes:
        language (str): The language for OCR processing.
        tesseract_path (str): Path to the Tesseract executable.
        poppler_path (str): Path to the Poppler utilities.
    """

    def __init__(self, language: str = DEFAULT_LANGUAGE) -> None:
        self.language: str = language
        self.tesseract_path: str = TESSERACT_PATH or self.find_tesseract()
        self.poppler_path: str = POPPLER_PATH or self.find_poppler()
        type_text(f"Tesseract path: {self.tesseract_path}", Fore.CYAN)
        type_text(f"Poppler path: {self.poppler_path}", Fore.CYAN)

    @staticmethod
    def find_program(program: str) -> Optional[str]:
        """
        Find the path of a program in the system.

        Args:
            program (str): The name of the program to find.

        Returns:
            Optional[str]: The path to the program if found, None otherwise.
        """
        logger.info(f"Searching for {program}")
        if sys.platform.startswith("win"):
            program += ".exe"

        for path in os.environ["PATH"].split(os.pathsep):
            exe_file: Path = Path(path) / program
            if exe_file.is_file() and os.access(str(exe_file), os.X_OK):
                logger.info(f"Found {program} in PATH: {exe_file}")
                return str(exe_file)

        common_dirs: List[Path] = [
            Path(os.environ.get("ProgramFiles", "C:/Program Files")),
            Path(os.environ.get("ProgramFiles(x86)", "C:/Program Files (x86)")),
            Path(os.environ.get("USERPROFILE", "~")) / "Downloads",
            Path("C:/Program Files/Tesseract-OCR"),
            Path("C:/Program Files/poppler/Library/bin"),
            Path("C:/Program Files/poppler/poppler-24.08.0/Library/bin"),
            Path("/usr/share/poppler"),
            Path("/usr/share/tesseract-ocr/5/tessdata"),
            Path("/usr/bin"),
            Path("/usr/local/bin"),
            Path("/usr/share"),
            Path("/opt"),
            Path.home() / "Downloads",
        ]

        for directory in common_dirs:
            exe_file = directory / program
            if exe_file.is_file() and os.access(str(exe_file), os.X_OK):
                logger.info(f"Found {program} in common directory: {exe_file}")
                return str(exe_file)

        logger.warning(f"{program} not found")
        return None

    def find_poppler(self) -> str:
        """Find the Poppler executable."""
        pdftoppm: Optional[str] = self.find_program("pdftoppm")
        if not pdftoppm:
            raise EnvironmentError(
                "Poppler (pdftoppm) not found. Please install it and make sure it's in your PATH."
            )
        return str(Path(pdftoppm).parent)

    def find_tesseract(self) -> str:
        """Find the Tesseract executable."""
        tesseract: Optional[str] = self.find_program("tesseract")
        if not tesseract:
            raise EnvironmentError(
                "Tesseract not found. Please install it and make sure it's in your PATH."
            )
        return tesseract

    def find_bengali_traineddata(self) -> Optional[str]:
        """Find the Bengali traineddata file."""
        possible_locations = [
            Path(self.tesseract_path).parent / "tessdata" / "ben.traineddata",
            Path("/usr/share/tesseract-ocr/5/tessdata/ben.traineddata"),
            Path("/usr/share/tesseract-ocr/4.00/tessdata/ben.traineddata"),
            Path("/usr/local/share/tessdata/ben.traineddata"),
            Path.home() / ".local/share/tessdata/ben.traineddata",
        ]

        for location in possible_locations:
            if location.is_file():
                logger.info(f"Found Bengali traineddata at: {location}")
                return str(location)

        logger.warning("Bengali traineddata not found")
        return None

    def convert_pdf_to_images(self, pdf_path: Path) -> List[Path]:
        """Convert a PDF file to a list of image files."""
        image_prefix: str = f"temp_image_{os.getpid()}"
        pdftoppm_path: str = os.path.join(self.poppler_path, "pdftoppm")
        logger.info(f"Converting PDF to images using {pdftoppm_path}")
        try:
            subprocess.run(
                [pdftoppm_path, "-png", str(pdf_path), image_prefix],
                check=True,
                capture_output=True,
                text=True,
            )
        except subprocess.CalledProcessError as e:
            logger.error(f"Error converting PDF to images: {e}")
            logger.error(f"pdftoppm stderr: {e.stderr}")
            raise
        return sorted(Path().glob(f"{image_prefix}-*.png"))

    def process_image(self, image_file: Path, page_num: int) -> str:
        """Process a single image file using OCR."""
        try:
            logger.info(f"Processing page {page_num}")
            result: subprocess.CompletedProcess = subprocess.run(
                [self.tesseract_path, str(image_file), "stdout", "-l", self.language],
                capture_output=True,
                check=True,
                encoding="utf-8",
            )
            text: str = result.stdout
            os.remove(image_file)
            return f"\n--- Page {page_num} ---\n{text}"
        except subprocess.CalledProcessError as e:
            logger.error(f"Error processing page {page_num}: {e}")
            logger.error(f"Tesseract stderr: {e.stderr}")
            return f"\n--- Page {page_num} ---\nError: {e}\n"

    def extract_text_from_pdf(
        self, pdf_path: str, output_file: Optional[str] = None
    ) -> str:
        """
        Extract text from a PDF file using OCR.

        Args:
            pdf_path (str): Path to the input PDF file.
            output_file (Optional[str]): Path to save the extracted text.

        Returns:
            str: The extracted text.
        """
        pdf_path_obj: Path = Path(pdf_path)
        output_file_obj: Path = (
            Path(output_file) if output_file else pdf_path_obj.with_suffix(".txt")
        )

        logger.info(f"Extracting text from {pdf_path_obj}")
        images: List[Path] = self.convert_pdf_to_images(pdf_path_obj)
        full_book: List[str] = [""] * len(images)

        with ThreadPoolExecutor() as executor:
            futures: Dict[Future[str], int] = {
                executor.submit(self.process_image, img, i): i
                for i, img in enumerate(images, start=1)
            }
            for future in tqdm(
                as_completed(futures), total=len(futures), desc="Processing pages"
            ):
                page_num: int = futures[future]
                try:
                    page_text: str = future.result()
                    full_book[page_num - 1] = page_text
                except Exception as exc:
                    logger.error(
                        f"Page {page_num} processing generated an exception: {exc}"
                    )
                    full_book[page_num - 1] = (
                        f"\n--- Page {page_num} ---\nError: {exc}\n"
                    )

        full_text: str = "".join(full_book)

        with open(output_file_obj, "w", encoding="utf-8") as file:
            file.write(full_text)

        logger.info(f"Text extracted and saved to {output_file_obj}")
        return full_text


def process_pdf(
    pdf_path: str, output_file: Optional[str] = None, language: str = "ben"
) -> str:
    """
    Process a PDF file and extract text using OCR.

    Args:
        pdf_path (str): Path to the input PDF file.
        output_file (Optional[str]): Path to save the extracted text.
        language (str): Language for OCR processing.

    Returns:
        str: The extracted text.
    """
    processor: OCRProcessor = OCRProcessor(language)
    type_text("Starting PDF processing...", Fore.GREEN)
    extracted_text: str = processor.extract_text_from_pdf(pdf_path, output_file)
    type_text(
        f"Extraction completed successfully. Processed file: {pdf_path}",
        Fore.GREEN,
    )
    return extracted_text


def main() -> None:
    """Main function to handle command-line interface."""
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Extract text from PDF using OCR"
    )
    parser.add_argument(
        "pdf_path",
        nargs="?",
        default=None,
        help="Path to the input PDF file",
    )
    parser.add_argument(
        "-o", "--output", help="Path to save the extracted text", default=None
    )
    parser.add_argument(
        "-l", "--language", default="ben", help="Language for OCR (default: ben)"
    )

    args: argparse.Namespace
    args, _ = parser.parse_known_args()

    if not args.pdf_path:
        try:
            default_pdf = pkgutil.get_data(__package__, "data/Freedom Fight.pdf")
            if default_pdf is None:
                raise FileNotFoundError(
                    "Default PDF 'Freedom Fight.pdf' not found in package data."
                )
            temp_pdf_path = Path.cwd() / "Freedom Fight.pdf"
            with open(temp_pdf_path, "wb") as f:
                f.write(default_pdf)
            args.pdf_path = str(temp_pdf_path)
            type_text("Using default PDF: Freedom Fight.pdf", Fore.CYAN)

            if not args.output:
                args.output = str(Path.cwd() / "Freedom Fight.txt")
        except Exception as e:
            logger.error(f"Failed to load default PDF: {e}")
            type_text(
                "Default PDF 'Freedom Fight.pdf' not found. Please provide a PDF file.",
                Fore.RED,
            )
            sys.exit(1)

    try:
        type_text("Bangla PDF OCR", Fore.YELLOW)
        type_text("----------------", Fore.YELLOW)
        extracted_text: str = process_pdf(args.pdf_path, args.output, args.language)
        type_text(
            f"Extraction completed successfully. Processed file: {args.pdf_path}",
            Fore.GREEN,
        )
        type_text(
            f"Extracted text saved to: {args.output or Path(args.pdf_path).with_suffix('.txt')}",
            Fore.GREEN,
        )
    except Exception as e:
        logger.error(f"An error occurred during extraction: {e}")
        type_text("An error occurred. Please check the log for details.", Fore.RED)


def setup_dependencies():
    """Set up and verify system dependencies for OCR processing."""
    system = platform.system().lower()
    print(Fore.YELLOW + Style.BRIGHT + "\nSystem Information:")
    print(
        Fore.WHITE
        + f"OS: {platform.system()} {platform.release()} {platform.version()}"
    )
    print(Fore.WHITE + f"Python: {platform.python_version()}")
    print(Fore.WHITE + f"Architecture: {platform.machine()}")

    print(Fore.YELLOW + Style.BRIGHT + "\nChecking system dependencies:")

    tesseract = OCRProcessor.find_program("tesseract")
    pdftoppm = OCRProcessor.find_program("pdftoppm")

    if system.startswith("win"):
        install_windows_dependencies(tesseract, pdftoppm)
    elif system.startswith("linux"):
        install_linux_dependencies(tesseract, pdftoppm)
    elif system.startswith("darwin"):
        install_macos_dependencies(tesseract, pdftoppm)
    else:
        print(
            Fore.YELLOW
            + f"Automatic dependency installation not supported for {system}."
        )
        show_manual_install_instructions()

    print(Fore.YELLOW + "\nVerifying installation:")
    verify_installation()


def install_windows_dependencies(tesseract, pdftoppm):
    """Install dependencies for Windows systems."""
    script_path = os.path.join(
        os.path.dirname(__file__), "scripts", "install_windows_dependencies.ps1"
    )
    if os.path.exists(script_path):
        print(Fore.CYAN + "Checking and installing missing dependencies for Windows...")
        try:
            subprocess.run(
                ["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path],
                check=True,
            )
            print(Fore.GREEN + "Windows dependencies check completed.")
        except subprocess.CalledProcessError as e:
            print(Fore.RED + f"Error checking/installing Windows dependencies: {e}")
            show_manual_install_instructions()
    else:
        print(
            Fore.RED
            + f"Windows dependency installation script not found at {script_path}"
        )
        show_manual_install_instructions()


def install_linux_dependencies(tesseract, pdftoppm):
    """Install dependencies for Linux systems."""
    if tesseract and pdftoppm:
        print(Fore.GREEN + "All required dependencies are already installed on Linux.")
        return

    print(Fore.CYAN + "Installing missing dependencies for Linux...")
    try:
        if not tesseract:
            subprocess.run(["sudo", "apt-get", "update"], check=True)
            subprocess.run(
                ["sudo", "apt-get", "install", "-y", "tesseract-ocr"], check=True
            )
            subprocess.run(
                ["sudo", "apt-get", "install", "-y", "tesseract-ocr-ben"], check=True
            )
        if not pdftoppm:
            subprocess.run(
                ["sudo", "apt-get", "install", "-y", "poppler-utils"], check=True
            )
        print(Fore.GREEN + "Linux dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"Error installing Linux dependencies: {e}")
        show_manual_install_instructions()


def install_macos_dependencies(tesseract, pdftoppm):
    """Install dependencies for macOS systems."""
    if tesseract and pdftoppm:
        print(Fore.GREEN + "All required dependencies are already installed on macOS.")
        return

    print(Fore.CYAN + "Installing missing dependencies for macOS...")
    try:
        if not tesseract:
            subprocess.run(["brew", "install", "tesseract"], check=True)
            subprocess.run(["brew", "install", "tesseract-lang"], check=True)
        if not pdftoppm:
            subprocess.run(["brew", "install", "poppler"], check=True)
        print(Fore.GREEN + "macOS dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"Error installing macOS dependencies: {e}")
        show_manual_install_instructions()


def verify_installation():
    """Verify the installation of Poppler and Tesseract, including Bengali language files."""
    pdftoppm = OCRProcessor.find_program("pdftoppm")
    tesseract = OCRProcessor.find_program("tesseract")
    system = platform.system().lower()

    if pdftoppm:
        print(Fore.GREEN + f"Poppler (pdftoppm) found at: {pdftoppm}")
    else:
        print(
            Fore.RED + "Poppler (pdftoppm) not found. Please check your installation."
        )

    if tesseract:
        print(Fore.GREEN + f"Tesseract found at: {tesseract}")
        bengali_lang = OCRProcessor().find_bengali_traineddata()
        if system.startswith("win"):
            tessdata_dir = Path(tesseract).parent / "tessdata"
            bengali_script = tessdata_dir / "script" / "Bengali.traineddata"
            if bengali_script.exists():
                print(Fore.GREEN + f"Bengali script data found at: {bengali_script}")
            else:
                print(
                    Fore.RED
                    + f"Bengali script data not found. Expected location: {bengali_script}"
                )

        if bengali_lang:
            print(Fore.GREEN + f"Bengali language data found at: {bengali_lang}")
        else:
            print(
                Fore.RED
                + "Bengali language data not found. Please check your Tesseract installation."
            )
    else:
        print(Fore.RED + "Tesseract not found. Please check your installation.")

    if system.startswith("win"):
        all_components_present = (
            pdftoppm
            and tesseract
            and bengali_script.exists()
            and bengali_lang
        )
    else:
        all_components_present = pdftoppm and tesseract and bengali_lang

    if all_components_present:
        print(Fore.GREEN + "All required components are present.")
    else:
        print(
            Fore.YELLOW
            + "Some components are missing. Please run the setup command again to install them."
        )


def show_manual_install_instructions():
    """Display manual installation instructions for the current operating system."""
    system = platform.system().lower()
    print(Fore.YELLOW + "\nManual Installation Instructions:")

    if system.startswith("linux"):
        print(Fore.CYAN + "For Linux (Ubuntu/Debian):")
        print("1. Install Tesseract OCR:")
        print("   sudo apt-get update")
        print("   sudo apt-get install tesseract-ocr")
        print("   sudo apt-get install tesseract-ocr-ben")
        print("2. Install Poppler utils:")
        print("   sudo apt-get install poppler-utils")

    elif system.startswith("darwin"):
        print(Fore.CYAN + "For macOS:")
        print("1. Install Homebrew if not already installed:")
        print(
            '   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
        )
        print("2. Install Tesseract OCR:")
        print("   brew install tesseract")
        print("   brew install tesseract-lang")
        print("3. Install Poppler:")
        print("   brew install poppler")

    elif system.startswith("win"):
        print(Fore.CYAN + "For Windows:")
        print("1. Install Tesseract OCR:")
        print(
            "   - Download the installer from: https://github.com/UB-Mannheim/tesseract/wiki"
        )
        print("   - Run the installer and make sure to add Tesseract to your PATH")
        print("2. Install Poppler:")
        print(
            "   - Download the latest release from: https://github.com/oschwartz10612/poppler-windows/releases"
        )
        print("   - Extract the contents to C:\\Program Files\\poppler")
        print("   - Add C:\\Program Files\\poppler\\Library\\bin to your PATH")
        print("3. Restart your command prompt or IDE after making these changes")

    else:
        print(
            Fore.YELLOW
            + f"Manual installation instructions not available for {system}."
        )

    print(
        Fore.WHITE
        + "\nAfter manual installation, run 'bangla-pdf-ocr-verify' to verify the installation."
    )


def verify_setup():
    """Verify the Bangla PDF OCR setup."""
    print(Fore.YELLOW + Style.BRIGHT + "\nVerifying Bangla PDF OCR Setup:")
    verify_installation()


if __name__ == "__main__":
    main()
