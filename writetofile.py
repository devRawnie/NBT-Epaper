import requests
from time import sleep
class Write:
    def __init__(self, url=None, filename=None):
        if url is not None:
            content = None
            count = 0
            while True:
                print("Status: GET Request to url: " + url)
                content = requests.get(url)
                print("Status: status code- %d" % content.status_code)
                if content.status_code == 200:
                    if filename is None:
                        filename = url.rsplit('/', 1)[-1]
                    self.__write(content, filename)
                    print("Status: Written {} to {}".format(url, filename))
                    break
                else:
                    if count > 2:
                        print("Error: Couldn't fetch page. unsuccessfull attempts: %d" % count)
                        break
                    count += 1
                    print("Error: Couldn't fetch page trying again in 5 seconds")
                    sleep(5)

        else:
            print("Error: No url given")
    
    def __write(self, content, filename):
        with open(filename, "wb") as f:
            for c in content:
                f.write(c)

#Write("http://image.epaper.navbharattimes.com/epaperimages//26032020//26032020-md-de.pdf")
