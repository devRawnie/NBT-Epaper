from epaperHandler import EPAPER
from datetime import datetime


if __name__ == "__main__":
    ob = EPAPER(publishDate=datetime())
    ob = EPAPER()
    ob.downloadPaper()
    