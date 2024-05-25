import argparse
import os
import tempfile
import html  # Dodaj ten import na górze skryptu

def extract_metadata_from_pdf(pdf_path):
    # Utworzenie tymczasowego pliku do przechowywania metadanych
    temp_file = tempfile.NamedTemporaryFile(delete=False).name

    # Używając pdftk, aby wyodrębnić metadane z pliku PDF
    cmd = f"pdftk {pdf_path} dump_data output {temp_file}"
    os.system(cmd)
    
    return temp_file


def generate_toc_from_metadata(metadata_path, output_path):
    with open(metadata_path, 'r') as meta_file:
        lines = meta_file.readlines()

    bookmarks = []
    for line in lines:
        if "BookmarkTitle" in line or "BookmarkPageNumber" in line or "BookmarkLevel" in line:
            bookmarks.append(line.strip())

    with open(output_path, 'w', encoding='utf-8') as out_file:
        i = 0
        while i < len(bookmarks):
            title = ""
            page = ""
            level = 0
            
            if "BookmarkTitle" in bookmarks[i]:
                title = bookmarks[i].split(":")[1].strip()
                title = html.unescape(title)
                i += 1
            if "BookmarkLevel" in bookmarks[i]:
                level = int(bookmarks[i].split(":")[1].strip()) - 1  # Odejmujemy 1, ponieważ pierwszy poziom to 0 wcięć/spacji
                i += 1
            if i < len(bookmarks) and "BookmarkPageNumber" in bookmarks[i]:
                page = bookmarks[i].split(":")[1].strip()
                i += 1
            
            out_file.write("  " * level + title + "||" + page + "\n")


def main():
    parser = argparse.ArgumentParser(description="Utwórz plik tekstowy ze spisem treści na podstawie metadanych pliku PDF.")
    parser.add_argument("pdf_path", help="Ścieżka do pliku PDF.")
    parser.add_argument("output_path", help="Ścieżka do wyjściowego pliku tekstowego.")

    args = parser.parse_args()

    metadata_file_path = extract_metadata_from_pdf(args.pdf_path)
    generate_toc_from_metadata(metadata_file_path, args.output_path)

    # Usuń tymczasowy plik metadanych
    os.remove(metadata_file_path)

if __name__ == "__main__":
    main()

