from datetime import datetime as dt
from os import listdir, stat
from os.path import join, exists
from pathlib import Path

from PyPDF2 import PdfMerger, PdfReader, PdfWriter


def merge(pathToFolder,filename):
    if pathToFolder is None:
        print("Error: No Path given")
        return False

    files = sorted(listdir(pathToFolder))
    if len(files) < 2:
        print("Error: Not enough files to merge")
        return False

    try:
        mergedObject = PdfMerger()
        for name in files:
            ext = Path(name).suffix
            if ext == ".pdf" and name != filename:
                print("Status: Merging file " + name)
                mergedObject.append(PdfReader(join(pathToFolder, name)))

        if filename is None:
            filename = dt.now().strftime("NBT %d %B %Y.pdf")
            print("Warning: No file name given. Using default filename %s" % filename)
        
        if Path(filename).suffix != ".pdf":
            print("Error: Invalid File Name")
            return False

        print("Status: Creating merged file '%s'" % filename)
        
        mergedObject.write(filename)
        mergedObject.close()

    except Exception as e:
        print("Error: Could not merge pdf files", e)
        return False

    return True

def get_file_size(path):
    size = -1
    if exists(path):
        st_size = stat(path).st_size
        size = st_size // (1024 * 1024)

    return size

def compress_pdf(file_to_compress, final_filename):
    try:
        if not file_to_compress:
            raise Exception(f"path-{file_to_compress} missing for the file to be compressed")

        print(f"compress_pdf: starting compression for {file_to_compress}. Initial size: {get_file_size(file_to_compress)}")
        reader = PdfReader(file_to_compress)
        writer = PdfWriter()
        count = 1
        for page in reader.pages:
            page.compress_content_streams()
            writer.add_page(page)
            print(f"compress_pdf: compressed page {count}")
            count += 1

        with open(final_filename, "wb") as f:
            writer.write(f)

        print("compress_pdf: successfully compressed")
    except Exception as compress_pdf_err:
        print(f"Error (compress_pdf): {compress_pdf_err}")

