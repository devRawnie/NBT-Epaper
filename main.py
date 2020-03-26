from bs4 import BeautifulSoup
import requests
from datetime import datetime as dt
from time import sleep
from os import mkdir

class EPAPER:
    base_url = "http://epaper.navbharattimes.com"
    delhi_edition = "13@13"
    date = "{day}@{month}@{year}"
    nbtepaper = "/paper/{pgno}-{edition}-{date}-1001.html"
    paper_path = ""

    def __init__(self):
        # print(self.__formatDate(dt.date(dt.now())))
        date = self.__formatDate(dt.now())
        if(len(date) > 0):
            self.date = self.date.format(day=date["day"],month=date["month"],year=date["year"])
            self.paper_path = date + "/"
        else:
            print("error: could not format date")
    
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
            mkdir(self.paper_path)

        else:
            sleep("error: could not establish page no's, trying again in 5 seconds")
            self.downloadPaper()

    def __fetch(self, page, content=None):
        if content is None:
            while content is None:
                response = requests.get(
                            self.base_url +
                            self.nbtepaper.format(
                                    pgno=page,
                                    edition=self.delhi_edition,
                                    date=self.date
                                )
                        )
                if response.status_code == 200:
                    content = response.text
                else:
                    print("error: no response recieved, trying again in 5 seconds")
                    sleep(5)

        filename = "nbt_{}.html".format(page)
        with open(filename, "w") as f:
            for text in response.text:
                f.write(text)                    
                # soup = BeautifulSoup(response.text, "html.parser")
                # print(soup.prettify())


ob = EPAPER()
# ob.fetch()
