import os
from PyPDF2 import PdfReader
from ebooklib import epub
import docx
from bs4 import BeautifulSoup


def setup_epub_book(identifier, title, language="en"):
    """
    Setup an EPUB book with the given identifier, title, and language.

    :param identifier: The identifier for the EPUB book.
    :param title: The title of the EPUB book.
    :param language: The language of the EPUB book.
    :return: An initialized EpubBook object.
    """
    ebook = epub.EpubBook()
    ebook.set_identifier(identifier)
    ebook.set_title(title)
    ebook.set_language(language)
    return ebook


def add_chapter(ebook, title, filename, content):
    """
    Add a chapter to the EPUB book.

    :param ebook: The EpubBook object.
    :param title: The title of the chapter.
    :param filename: The filename for the chapter.
    :param content: The content of the chapter.
    """
    if not content.strip():
        return None
    chapter = epub.EpubHtml(title=title, file_name=filename)
    chapter.content = f"<h1>{title}</h1>{content}"
    ebook.add_item(chapter)
    return chapter


def finalize_epub_book(ebook, spine, toc, output_path):
    """
    Finalize and write the EPUB book to the specified output path.

    :param ebook: The EpubBook object.
    :param spine: The spine (order) of the chapters.
    :param toc: The table of contents for the book.
    :param output_path: The output path for the EPUB file.
    """
    ebook.toc = toc
    ebook.spine = spine
    ebook.add_item(epub.EpubNcx())
    ebook.add_item(epub.EpubNav())
    style = "BODY { font-family: Arial, sans-serif; }"
    nav_css = epub.EpubItem(
        uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style
    )
    ebook.add_item(nav_css)
    epub.write_epub(output_path, ebook, {})


def pdf_to_epub(pdf_path, epub_path):
    """
    Convert a PDF file to an EPUB file.

    :param pdf_path: The path to the PDF file.
    :param epub_path: The path to the output EPUB file.
    """
    reader = PdfReader(pdf_path)
    book_title = os.path.splitext(os.path.basename(pdf_path))[0]
    ebook = setup_epub_book(book_title, book_title)

    spine = ["nav"]
    toc = []

    content = ""
    for page_num, page in enumerate(reader.pages):
        text = page.extract_text()
        content += f"<h2>Page {page_num + 1}</h2><p>{text}</p>"

    chapter_title = book_title
    filename = "content.xhtml"
    chapter = add_chapter(ebook, chapter_title, filename, content)
    if chapter:
        spine.append(chapter)
        toc.append(epub.Link(filename, chapter_title, filename))

    finalize_epub_book(ebook, spine, toc, epub_path)


def docx_to_epub(docx_path, epub_path):
    """
    Convert a DOCX file to an EPUB file.

    :param docx_path: The path to the DOCX file.
    :param epub_path: The path to the output EPUB file.
    """
    doc = docx.Document(docx_path)
    book_title = os.path.splitext(os.path.basename(docx_path))[0]
    ebook = setup_epub_book(book_title, book_title)

    spine = ["nav"]
    toc = []

    content = ""
    for para in doc.paragraphs:
        if para.text.strip():
            content += f"<p>{para.text}</p>"

    chapter_title = book_title
    filename = "content.xhtml"
    chapter = add_chapter(ebook, chapter_title, filename, content)
    if chapter:
        spine.append(chapter)
        toc.append(epub.Link(filename, chapter_title, filename))

    finalize_epub_book(ebook, spine, toc, epub_path)


def html_to_epub(html_path, epub_path):
    """
    Convert an HTML file to an EPUB file.

    :param html_path: The path to the HTML file.
    :param epub_path: The path to the output EPUB file.
    """
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        content = str(soup.body)

    book_title = os.path.splitext(os.path.basename(html_path))[0]
    ebook = setup_epub_book(book_title, book_title)

    spine = ["nav"]
    toc = []

    chapter_title = book_title
    filename = "content.xhtml"
    chapter = add_chapter(ebook, chapter_title, filename, content)
    if chapter:
        spine.append(chapter)
        toc.append(epub.Link(filename, chapter_title, filename))

    finalize_epub_book(ebook, spine, toc, epub_path)


def txt_to_epub(txt_path, epub_path):
    """
    Convert a TXT file to an EPUB file.

    :param txt_path: The path to the TXT file.
    :param epub_path: The path to the output EPUB file.
    """
    with open(txt_path, "r", encoding="utf-8") as f:
        content = f.read()

    book_title = os.path.splitext(os.path.basename(txt_path))[0]
    ebook = setup_epub_book(book_title, book_title)

    spine = ["nav"]
    toc = []

    chapter_title = book_title
    filename = "content.xhtml"
    chapter = add_chapter(
        ebook, chapter_title, filename, content.replace("\n", "<br/>")
    )
    if chapter:
        spine.append(chapter)
        toc.append(epub.Link(filename, chapter_title, filename))

    finalize_epub_book(ebook, spine, toc, epub_path)
