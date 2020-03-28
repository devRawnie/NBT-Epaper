from epaperHandler import EPAPER
from datetime import datetime
import re
import sys

def validate(date):
    pattern = "^\d{1,2}/\d{1,2}/\d{4}$"
    if re.search(pattern, date) is None:
        return False
    d = list(map(int, date.split("/")))
    if d[0] in range(1,31 + 1) and d[1] in range(1,12 + 1) and d[2] > 2018:
        return d
    else:
        print("Error: Date values out of range")
        return False 

if __name__ == "__main__":
    publishDate = None
    if len(sys.argv) > 1:
        date = validate( str(sys.argv[1]) )
        if date:
            publishDate = datetime(date[2], date[1], date[0])
        else:
            print("Error: Invalid date argument passed") 
            exit(0)        
        publishDate = datetime(date[2], date[1], date[0])
    
    if publishDate is None:
        publishDate = datetime.now()
    ob = EPAPER(publishDate=publishDate)
    ob.downloadPaper()
    