from epaperHandler import EPAPER
from mergePDF import Merge
ob = EPAPER()
# ob.downloadPaper()
Merge(ob.paper_path)