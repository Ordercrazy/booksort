import os
import zipfile
from ebooklib import epub
from bs4 import BeautifulSoup

def extract_epub_data(epub_path):
    """
    Extracts metadata and the first 50kb of text from an EPUB file.

    Args:
        epub_path (str): The path to the .epub file.

    Returns:
        tuple: A tuple containing the metadata dictionary and the extracted text string.
    """
    try:
        book = epub.read_epub(epub_path)
    except zipfile.BadZipFile:
        return None, "Error: The file is not a valid EPUB file or is corrupted."

    # Extract all metadata from the OPF file
    metadata = {}
    for meta in book.get_metadata('DC', None):
        metadata[meta[0]] = meta[1]

    # Extract the first 50kb of text
    text_content = ""
    text_size = 0
    limit = 50 * 1024  # 50kb

    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        if text_size >= limit:
            break

        content = item.get_content()
        soup = BeautifulSoup(content, 'html.parser')

        for p in soup.find_all('p'):
            if text_size >= limit:
                break
            
            paragraph_text = p.get_text(separator=' ', strip=True)
            if paragraph_text:
                # Ensure a space follows the paragraph
                text_to_add = paragraph_text + '\n\n'
                text_content += text_to_add
                text_size += len(text_to_add.encode('utf-8'))

    return metadata, text_content[:limit]

def find_and_process_epub():
    """
    Finds the first .epub file in the current directory and processes it.
    """
    for file in os.listdir('.'):
        if file.endswith('.epub'):
            print(f"Found EPUB file: {file}\n")
            metadata, text = extract_epub_data(file)

            if metadata is not None:
                print("--- Metadata ---")
                for key, value in metadata.items():
                    print(f"{key}: {value}")
                
                print("\n--- First 50kb of Text ---")
                print(text)
            else:
                print(text)
            return

    print("No .epub file found in the current directory.")

if __name__ == '__main__':
    find_and_process_epub()
