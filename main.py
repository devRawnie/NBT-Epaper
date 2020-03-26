from bs4 import BeautifulSoup
import requests
from datetime import datetime as dt
from time import sleep
from os import mkdir
from os.path import isdir 
from writetofile import Write

class EPAPER:
    base_url = "http://epaper.navbharattimes.com"
    pdf_url = "http://image.epaper.navbharattimes.com/epaperimages//{date}//{date}-md-de-"
    delhi_edition = "13@13"
    date = "{day}@{month}@{year}"
    nbtepaper = "/paper/{pgno}-{edition}-{date}-1001.html"
    paper_path = ""

    def __init__(self):
        date = self.__formatDate(dt.now())
        if(len(date) > 0):
            self.date = self.date.format(day=date["day"],month=date["month"],year=date["year"])
            self.paper_path = self.date + "/"
            print("Status: Date set: " + self.date)
        else:
            print("Error: could not format date")
    
    def __formatDate(self, date):
        d = {}
        if date is not None:
            d["day"] = "{:02d}".format(date.day)
            d["month"]  = "{:02d}".format(date.month)
            d["year"] = "{:04d}".format(date.year)
        else:
            print("Invalid date argument passed")
        return d

    def downloadPaper(self):
        response = requests.get(
                    self.base_url +
                    self.nbtepaper.format(
                            pgno=1,
                            edition=self.delhi_edition,
                            date=self.date
                        )
                )
        if response.status_code == 200:
            if not isdir(self.paper_path):
                mkdir(self.paper_path)
            soup = BeautifulSoup(response.text, "html.parser")
            span = soup.findAll("span", {"class":"headforpagenext"})
            print("Total {} pages".format( len(span) + 1) )
            self.__fetch(len(span) + 1)
        else:
            sleep("Error: could not establish value for page no's, trying again in 5 seconds")
            self.downloadPaper()

    def __generatePDFURL(self, date, page):
        date = self.__formatDate(dt.now())
        datestring = date["day"] + date["month"] + date["year"]
        self.pdf_url = self.pdf_url.format(date=datestring)
        return self.pdf_url + str(page) + ".pdf"

    def __fetch(self, page):
        for pageno in range(1,page+1):
            content = None
            while content is None:
                print("Status: Fetching page no %d" % pageno)
                response = requests.get(
                            self.base_url +
                            self.nbtepaper.format(
                                    pgno=pageno,
                                    edition=self.delhi_edition,
                                    date=self.date
                                )
                        )
                if response.status_code == 200:
                    content = response.text
                    break
                else:
                    print("Error: no response recieved on page %d, trying again in 5 seconds" % pageno)
                    sleep(5)
            if content is not None:     
                filename = self.paper_path + "nbt_{}.pdf".format(pageno)
                url = self.__generatePDFURL(dt.now(), pageno)
                print("Status: Generating File-{}".format(filename))
                Write(filename=filename, url=url)
        print("Status: Finished")

ob = EPAPER()
# ob.fetch()
ob.downloadPaper()