import os
import re
import argparse

def generate_metadata_from_toc(toc_path, offset):  # Dodanie parametru offset
    with open(toc_path, 'r') as toc_file:
        toc_lines = toc_file.readlines()

    metadata_path = "temp_metadata.txt"
    
    with open(metadata_path, 'w') as metadata_file:
        for line in toc_lines:
            stripped_line = line.strip()

            # Ignoruj puste linie
            if not stripped_line:
                continue

            # Zakładaj, że domyślnie nie ma numeru strony
            title, page_num = stripped_line, None

            if "||" in stripped_line:
                parts = stripped_line.split("||")
                if len(parts) != 2:
                    print(f"Błąd w linii: '{stripped_line}'. Nieprawidłowy format.")
                    continue
                title, page_num = parts
                
                # Dodaj przesunięcie do numeru strony
                try:
                    page_num = str(int(page_num) + offset)
                except ValueError:
                    print(f"Błąd w linii: '{stripped_line}'. Nieprawidłowy numer strony.")
                    continue
            
            indentation = len(line) - len(line.lstrip(' '))
            level = indentation // 2

            bookmark_line = f"BookmarkBegin\nBookmarkTitle: {title}\nBookmarkLevel: {level + 1}\n"
            if page_num:
                bookmark_line += f"BookmarkPageNumber: {page_num}\n"
            metadata_file.write(bookmark_line)
    
    return metadata_path

def add_metadata_to_pdf(pdf_path, metadata_path):
    updated_pdf_path = "updated_" + os.path.basename(pdf_path)
    os.system(f"pdftk {pdf_path} update_info {metadata_path} output {updated_pdf_path}")

def main():
    parser = argparse.ArgumentParser(description="Utwórz metadane dla pliku PDF na podstawie pliku tekstowego ze spisem treści.")
    parser.add_argument("pdf_path", help="Ścieżka do pliku PDF.")
    parser.add_argument("toc_path", help="Ścieżka do pliku tekstowego ze spisem treści.")
    parser.add_argument("offset", type=int, nargs='?', default=0, help="Liczba dodawana do numeru strony zakładki.")

    args = parser.parse_args()

    metadata_file_path = generate_metadata_from_toc(args.toc_path, args.offset)  # Przekazanie offset jako argumentu
    add_metadata_to_pdf(args.pdf_path, metadata_file_path)

    # Usuń tymczasowy plik metadanych
    os.remove(metadata_file_path)

if __name__ == "__main__":
    main()

