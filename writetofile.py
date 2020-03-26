import requests
from time import sleep
def write(url=None, filename=None):
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
                with open(filename, "wb") as f:
                    for c in content:
                        f.write(c)
                print("Status: Written {} to {}".format(url, filename))
                return True
            else:
                if count > 2:
                    print("Error: Couldn't fetch pdf. unsuccessfull attempts: %d" % count)
                    return False
                count += 1
                print("Error: Couldn't fetch pdf trying again in 5 seconds")
                sleep(5)

    else:
        print("Error: No url given")
    

