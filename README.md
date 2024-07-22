# Universal EPUB Converter

## Overview

This project provides a script to convert various document formats (PDF, DOCX, HTML, TXT) into EPUB format. The primary goal is to automate the conversion process, though the final output might not be of the highest quality due to the automatic nature of the conversion.

## Features

-   Converts PDF, DOCX, HTML, and TXT files to EPUB format.
-   Handles bulk conversion, prioritizing file types as follows:
    1. DOCX
    2. HTML
    3. TXT
    4. PDF

## Usage

1. **Download the executable** from the [releases page](https://github.com/jiuvirgil/universal-epub-converter/releases).
2. **Move the executable to the directory where your files are located.**.
3. **Run the executable**.
4. **Check the same directory for the output EPUB files.**.

## Development and Building

To develop and build the executable yourself, follow these steps:

1. **Clone the repository**:

    ```bash
    git clone https://github.com/jiuvirgil/universal-epub-converter.git
    cd universal-epub-converter
    ```

2. **Create and activate a virtual environment**:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Build the executable using PyInstaller**:
    ```bash
    pyinstaller --onefile convert_to_epub.py
    ```

## Testing

1. **Add test documents to the `test_files` directory**.
2. **Run the tests**:
    ```bash
    python test_conversion.py
    ```

## Acknowledgements

-   Test files are sourced from [Project Gutenberg](https://www.gutenberg.org/).

## To Do

-   [ ] Replicate the current directory instead of making duplicates.
-   [ ] Add support for multiple languages.
-   [ ] Implement tests for multiple languages.

## Script Files

-   **`convert_to_epub.py`**: The main script to convert files to EPUB format.
-   **`converters.py`**: Contains the conversion functions for each file type.
-   **`test_conversion.py`**: Script to run tests on the conversion functions.

## Recommendation

For the best reading experience, we recommend using [Aquile Reader](https://www.aquilereader.com).
