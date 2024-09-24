import requests
import shutil

from time import sleep

def write(url, filename):
    flag = True
    try:
        if filename is None:
            filename = url.rsplit('/', 1)[-1]

        print("Status: GET Request to url: " + url)
        with requests.get(url, stream=True) as r:
            with open(filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

    except Exception as write_err:
        print(f"Error: could not write {url} to {filename}: {write_err}")
        flag = False

    return flag
