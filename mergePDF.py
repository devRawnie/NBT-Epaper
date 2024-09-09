from datetime import datetime as dt
from os import listdir
from os.path import join
from pathlib import Path

from PyPDF2 import PdfMerger, PdfReader


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
