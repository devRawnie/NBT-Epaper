from PyPDF2 import PdfFileMerger, PdfFileReader
from os import listdir
from os.path import join
from pathlib import Path
from datetime import datetime as dt
def merge(pathToFolder=None, filename=None):
    if pathToFolder is None:
        print("Error: No Path given")
        return False
    files = sorted(listdir(pathToFolder))
    if len(files) < 2:
        print("Error: Not enough files to merge")
        return False
    mergedObject = PdfFileMerger()
    for name in files:
        ext = Path(name).suffix
        if ext == ".pdf" and name != filename:
            print("Status: Merging file " + name)
            mergedObject.append(PdfFileReader(join(pathToFolder, name)))
    if filename is None:
        d = dt.now()
        filename = d.strftime("NBT %d %B %Y.pdf")
    if Path(filename).suffix != ".pdf":
        print("Error: Invalid File Name")
        return False
    print("Status: Creating merged file '%s'" % filename)
    mergedObject.write(filename)
    return True