from PyPDF2 import PdfFileMerger, PdfFileReader
from os import listdir
from os.path import join
from pathlib import Path
class Merge:
    def __init__(self, pathToFolder=None, filename=None):
        if pathToFolder is None:
            print("No Path given containing pdfs")
        files = sorted(listdir(pathToFolder))
        mergedObject = PdfFileMerger()
        for name in files:
            ext = Path(name).suffix
            if ext == ".pdf" and name != filename:
                print("Status: Merging file " + name)
                mergedObject.append(PdfFileReader(join(pathToFolder, name)))
        if filename is None:
            filename = join(pathToFolder, "merged.pdf")
        mergedObject.write(filename)