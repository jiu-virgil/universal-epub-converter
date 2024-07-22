import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import colorlog
import logging
from converters import pdf_to_epub, docx_to_epub, html_to_epub, txt_to_epub

# Setup logger
handler = colorlog.StreamHandler()
handler.setFormatter(
    colorlog.ColoredFormatter("%(log_color)s%(levelname)s: %(message)s")
)

logger = colorlog.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def process_file(file_path, convert_function, root_folder):
    """
    Process a file for conversion and log the result.

    :param file_path: The path to the file to convert.
    :param convert_function: The conversion function to use.
    :param root_folder: The root folder for relative path calculations.
    """
    relative_path = os.path.relpath(file_path, root_folder)
    epub_path = os.path.join(
        os.getcwd(), f"{os.path.splitext(os.path.basename(file_path))[0]}.epub"
    )
    try:
        convert_function(file_path, epub_path)
        logger.info(
            f"Successfully converted {relative_path} to \033[4m{os.path.basename(epub_path)}\033[0m"
        )
    except Exception as e:
        logger.error(f"Failed to convert {relative_path}: {e}")


def convert_all_to_epub(root_folder):
    """
    Convert all supported files in the directory and subdirectories to EPUB format,
    prioritizing the format that supports the most features if duplicate filenames exist.

    :param root_folder: The root directory to start the conversion.
    """

    def is_supported_file(filename):
        """
        Check if the file is supported for conversion.

        :param filename: The name of the file to check.
        :return: True if the file is supported, False otherwise.
        """
        return filename.lower().endswith((".pdf", ".docx", ".html", ".txt"))

    file_converters = {
        ".pdf": pdf_to_epub,
        ".docx": docx_to_epub,
        ".html": html_to_epub,
        ".txt": txt_to_epub,
    }

    found_files = False
    file_groups = {}

    for dirpath, dirnames, filenames in os.walk(root_folder):
        # Skip the venv folder
        if "venv" in dirnames:
            dirnames.remove("venv")

        for filename in filenames:
            if is_supported_file(filename):
                found_files = True
                file_extension = os.path.splitext(filename)[1].lower()
                file_base = os.path.splitext(filename)[0].lower()
                file_path = os.path.join(dirpath, filename)

                if file_base not in file_groups:
                    file_groups[file_base] = {}

                file_groups[file_base][file_extension] = file_path

    if not found_files:
        logger.info("No compatible files found to convert.")
        return

    # Prioritize and convert files
    priority_order = [".docx", ".html", ".txt", ".pdf"]
    files_to_process = []
    for file_base, formats in file_groups.items():
        for extension in priority_order:
            if extension in formats:
                files_to_process.append(
                    (formats[extension], file_converters[extension])
                )
                break

    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(
                process_file, file_path, convert_function, root_folder
            ): file_path
            for file_path, convert_function in files_to_process
        }

        for future in as_completed(futures):
            file_path = futures[future]
            try:
                future.result()
            except Exception as e:
                logger.error(f"Error processing {file_path}: {e}")


if __name__ == "__main__":
    try:
        convert_all_to_epub(os.getcwd())
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        input("Press Enter to exit...")
        sys.exit(1)
    sys.exit(0)
