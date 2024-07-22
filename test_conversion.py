import os
import unittest
from converters import pdf_to_epub, docx_to_epub, html_to_epub, txt_to_epub


class TestEPUBConversion(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Set up test environment by specifying the test directory and test files.
        """
        cls.test_dir = "test_files"
        cls.output_dir = "converted_files"

        # Ensure the output directory exists
        os.makedirs(cls.output_dir, exist_ok=True)

        # Clear out existing files in the output directory
        for file in os.listdir(cls.output_dir):
            file_path = os.path.join(cls.output_dir, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error: {e}")

        cls.test_files = [
            ("Dracula by Bram Stoker.docx", docx_to_epub),
            ("Pride and Prejudice by Jane Austen.html", html_to_epub),
            ("Moby Dick; Or, The Whale by Herman Melville.txt", txt_to_epub),
            ("Beauty and the Beast by Anonymous.pdf", pdf_to_epub),
        ]

    def test_files_to_epub(self):
        """
        Test converting various file formats to EPUB.
        """
        for file_name, convert_function in self.test_files:
            file_path = os.path.join(self.test_dir, file_name)
            if not os.path.exists(file_path):
                self.fail(f"Test file {file_path} does not exist.")
            epub_path = os.path.join(
                self.output_dir,
                os.path.splitext(os.path.basename(file_path))[0] + ".epub",
            )
            convert_function(file_path, epub_path)
            self.assertTrue(os.path.exists(epub_path))


if __name__ == "__main__":
    unittest.main()
