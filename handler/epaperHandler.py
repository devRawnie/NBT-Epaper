import re
import shutil

from bs4 import BeautifulSoup
from datetime import datetime as dt
from os import mkdir
from os.path import isdir 
from requests import get
from time import sleep

from writetofile import write
from mergePDF import merge

class EPAPER:
    
    def __init__(self, publishDate, edition=None):
        self.base_url = "https://epaper.navbharattimes.com/{state}/{date}/{edition_num}/page-{pgno}.html"
        self.pdf_url = "https://image.mepaper.navbharattimes.com/epaperimages/{date}/{date}-md-{region}-"
        self.region = "de" # "mu"
        self.edition = "13@13"
        self.state = "delhi"
        self.edition_num = 13 # 16
        self.in_date_format = "{day}_{month}_{year}"
        self.iso_date_format = "{year}-{month}-{day}"

        self.paper_path = ""
        self.publishDate = None
        if not isinstance(publishDate, dt):
            print("Error: Invalid date entered")
            return

        if edition is not None and self.__is_valid_edition(edition):
            self.edition = edition
            print("Status: Setting edition: %s" % edition)

        self.publishDate = publishDate
        date = self.__formatDate(publishDate)
        
        if len(date) == 0:
            return print("Error: Could not format date")

        self.iso_date = self.iso_date_format.format(day=date["day"],month=date["month"],year=date["year"])
        self.in_date = self.in_date_format.format(day=date["day"],month=date["month"],year=date["year"])

        self.paper_path = f"/tmp/{self.in_date}/"
        print("Status: Date set: " + self.in_date)
    
    def __is_valid_edition(self, edition):
        pattern = re.compile("^\\d{1,2}@\\d{2}$")
        return True if pattern.search(edition) else False
    
    def get_paper_path(self):
        return self.paper_path

    def __formatDate(self, date):
        d = {}
        if date is not None:
            d["day"] = "{:02d}".format(date.day)
            d["month"]  = "{:02d}".format(date.month)
            d["year"] = "{:04d}".format(date.year)
        else:
            print("Error: Invalid date argument passed")
        return d

    def downloadPaper(self, count=-1):
        count += 1
        if count > 2:
            print("Error: Unable to download newspaper for this date")
            return False

        request_url = self.base_url.format(pgno=1, edition_num=self.edition_num, date=self.iso_date, state=self.state)
        response = get(request_url)

        if response.status_code != 200:
            print("Error: could not establish value for page no's, trying again in 5 seconds")
            sleep(5)
            return self.downloadPaper(count+1)

        if not isdir(self.paper_path):
            mkdir(self.paper_path)

        soup = BeautifulSoup(response.text, "html.parser")
        input_tag = soup.findAll("input", {"id":"totalpages"})
        pages = input_tag[0]['value']
        if not pages:
            print("Error: Unable to download newspaper for this date")
            return False

        print(f"Total {pages} pages")
        return self.__fetch(int(pages))

    def __generatePDFURL(self, page):
        date = self.__formatDate(self.publishDate)
        datestring = date["day"] + date["month"] + date["year"]
        pdf_url = self.pdf_url.format(date=datestring, region=self.region)
        return f"{pdf_url}{page}.pdf"

    def __fetch(self, pages):
        result = False
        try:
            for pageno in range(1, pages+1):
                content = None
                print("Status: Fetching page no {} of {}".format(pageno, pages))
                request_url = self.base_url.format(pgno=pageno, edition_num=self.edition_num, date=self.iso_date, state=self.state)
                response = get(request_url)
                if response.status_code != 200:
                    raise Exception(f"Error: no response recieved on page {pageno}")

                filename = self.paper_path + "{:02d}.pdf".format(pageno)
                url = self.__generatePDFURL(pageno)
                print(f"Status: Generating File - {filename}")
                if not write(filename=filename, url=url):
                    raise Exception("Error: Could not download newspaper for this date")

            filename = "/tmp/" + self.publishDate.strftime("NBT %d %B %Y.pdf")
            if not merge(self.paper_path, filename):
                raise Exception("Error: Could not create PDF for newspaper")

            result = filename
        except Exception as e:
            print("Error in __fetch:", e)
            result = False

        finally:
            try:
                shutil.rmtree(self.paper_path, ignore_errors=True)
            except Exception as shutil_error:
                print("Error in clearing newspaper folder:", shutil_error)

            return result

