'''
get_jps.py

TODO(IK) here put description of file
'''
import os
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile
import json

def get_jps(url, path):
    '''
    download jps bible located at url to path
    '''
    if os.path.exists(path):
        print('"%s" exists. cancelling download.'%path)
        return
    os.mkdir(path)
    with urlopen(url) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            zfile.extractall(path)

def main():
    '''
    runs get_jps() according to config file.
    '''
    with open("config.json") as config:
        options = json.load(config)
    get_jps(options["jps_url"], options["local_jps_html"])

if __name__ == "__main__":
    main()
