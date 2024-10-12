from setuptools import setup, find_packages
from setuptools.command.install import install
import platform
import subprocess
import os
import sys
from colorama import init, Fore, Style

init(autoreset=True)


class PostInstallCommand(install):
    def run(self):
        install.run(self)
        self.install_dependencies()

    def install_dependencies(self):
        system = platform.system().lower()
        print(Fore.YELLOW + Style.BRIGHT + "\nSystem Information:")
        print(
            Fore.WHITE
            + f"OS: {platform.system()} {platform.release()} {platform.version()}"
        )
        print(Fore.WHITE + f"Python: {sys.version}")
        print(Fore.WHITE + f"Architecture: {platform.machine()}")

        print(Fore.YELLOW + Style.BRIGHT + "\nInstalling system dependencies:")

        if system.startswith("linux"):
            self.install_linux_dependencies()
        elif system.startswith("darwin"):
            self.install_macos_dependencies()
        elif system.startswith("win"):
            self.show_windows_instructions()
        else:
            print(
                Fore.YELLOW
                + f"Automatic dependency installation not supported for {system}."
            )

        print(Fore.YELLOW + "\nPlease ensure all required dependencies are installed.")
        print(
            Fore.WHITE
            + "For detailed instructions, visit: "
            + Fore.GREEN
            + "https://github.com/asiff00/bangla-pdf-ocr"
        )

    def install_linux_dependencies(self):
        script_path = os.path.join(
            os.path.dirname(__file__),
            "bangla_pdf_ocr",
            "scripts",
            "install_linux_dependencies.sh",
        )
        if os.path.exists(script_path):
            print(Fore.CYAN + "Installing dependencies for Linux...")
            try:
                subprocess.run(["bash", script_path], check=True)
                print(Fore.GREEN + "Linux dependencies installed successfully.")
            except subprocess.CalledProcessError as e:
                print(Fore.RED + f"Error installing Linux dependencies: {e}")
        else:
            print(
                Fore.RED
                + f"Linux dependency installation script not found at {script_path}"
            )

    def install_macos_dependencies(self):
        script_path = os.path.join(
            os.path.dirname(__file__),
            "bangla_pdf_ocr",
            "scripts",
            "install_macos_dependencies.sh",
        )
        if os.path.exists(script_path):
            print(Fore.CYAN + "Installing dependencies for macOS...")
            try:
                subprocess.run(["bash", script_path], check=True)
                print(Fore.GREEN + "macOS dependencies installed successfully.")
            except subprocess.CalledProcessError as e:
                print(Fore.RED + f"Error installing macOS dependencies: {e}")
        else:
            print(
                Fore.RED
                + f"macOS dependency installation script not found at {script_path}"
            )

    def show_windows_instructions(self):
        print(Fore.RED + "IMPORTANT: For Windows users:")
        print(Fore.RED + "1. Activate your project environment (if using one)")
        print(Fore.RED + "2. Open PowerShell or Command Prompt as administrator")
        print(Fore.RED + "3. Run the command: bangla-pdf-ocr-setup")


def main_setup_dependencies():
    system = platform.system().lower()
    print(Fore.YELLOW + Style.BRIGHT + "\nSystem Information:")
    print(
        Fore.WHITE
        + f"OS: {platform.system()} {platform.release()} {platform.version()}"
    )
    print(Fore.WHITE + f"Python: {sys.version}")
    print(Fore.WHITE + f"Architecture: {platform.machine()}")

    print(Fore.YELLOW + Style.BRIGHT + "\nInstalling system dependencies:")

    if system.startswith("linux"):
        install_linux_dependencies()
    elif system.startswith("darwin"):
        install_macos_dependencies()
    elif system.startswith("win"):
        show_windows_instructions()
    else:
        print(
            Fore.YELLOW
            + f"Automatic dependency installation not supported for {system}."
        )

    print(Fore.YELLOW + "\nPlease ensure all required dependencies are installed.")
    print(
        Fore.WHITE
        + "If you're still struggling with the setup, you may find helpful information at: "
        + Fore.GREEN
        + "https://github.com/asiff00/bangla-pdf-ocr"
    )


def install_linux_dependencies():
    script_path = os.path.join(
        os.path.dirname(__file__),
        "bangla_pdf_ocr",
        "scripts",
        "install_linux_dependencies.sh",
    )
    if os.path.exists(script_path):
        print(Fore.CYAN + "Installing dependencies for Linux...")
        try:
            subprocess.run(["bash", script_path], check=True)
            print(Fore.GREEN + "Linux dependencies installed successfully.")
        except subprocess.CalledProcessError as e:
            print(Fore.RED + f"Error installing Linux dependencies: {e}")
    else:
        print(
            Fore.RED
            + f"Linux dependency installation script not found at {script_path}"
        )


def install_macos_dependencies():
    script_path = os.path.join(
        os.path.dirname(__file__),
        "bangla_pdf_ocr",
        "scripts",
        "install_macos_dependencies.sh",
    )
    if os.path.exists(script_path):
        print(Fore.CYAN + "Installing dependencies for macOS...")
        try:
            subprocess.run(["bash", script_path], check=True)
            print(Fore.GREEN + "macOS dependencies installed successfully.")
        except subprocess.CalledProcessError as e:
            print(Fore.RED + f"Error installing macOS dependencies: {e}")
        else:
            print(
                Fore.RED
                + f"macOS dependency installation script not found at {script_path}"
            )


def show_windows_instructions():
    print(Fore.CYAN + "For Windows users:")
    print(
        Fore.WHITE
        + "1. Download and install Tesseract: "
        + Fore.GREEN
        + "https://github.com/UB-Mannheim/tesseract/wiki"
    )
    print(
        Fore.WHITE
        + "2. Download and install Poppler: "
        + Fore.GREEN
        + "https://github.com/oschwartz10612/poppler-windows/releases"
    )
    print(
        Fore.WHITE
        + "3. Add the bin directories of both Tesseract and Poppler to your system PATH."
    )
    print(Fore.WHITE + "4. Download Bengali language data file (ben.traineddata) from:")
    print(
        Fore.GREEN
        + "   https://github.com/tesseract-ocr/tessdata/blob/main/ben.traineddata"
    )
    print(Fore.WHITE + "   and place it in the Tesseract 'tessdata' directory.")
    print(
        Fore.YELLOW
        + "5. Restart your command prompt or IDE after making these changes."
    )


setup(
    name="bangla-pdf-ocr",
    version="0.1.1",
    author="Abdullah Al Asif",
    author_email="asif.dev.bd@gmail.com",
    description="A package to extract Bengali text from PDFs using OCR",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/asiff00/bangla-pdf-ocr",
    packages=find_packages(include=["bangla_pdf_ocr", "bangla_pdf_ocr.*"]),
    include_package_data=True,
    package_data={
        "bangla_pdf_ocr": [
            "scripts/*",
            "data/*",
        ],
    },
    install_requires=[
        "tqdm",
        "Pillow",
        "pdf2image",
        "pytesseract",
        "colorama",
    ],
    entry_points={
        "console_scripts": [
            "bangla-pdf-ocr=bangla_pdf_ocr.ocr:main",
            "bangla-pdf-ocr-setup=bangla_pdf_ocr.ocr:setup_dependencies",
            "bangla-pdf-ocr-verify=bangla_pdf_ocr.ocr:verify_installation",
        ],
    },
    cmdclass={
        "install": PostInstallCommand,
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
