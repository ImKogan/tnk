import os
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile

current_directory = os.getcwd()
final_directory = os.path.join(current_directory, r'JPS')
if not os.path.exists(final_directory):
	os.makedirs(final_directory)

zipurl = 'http://www.mechon-mamre.org/htmlzips/et002.zip'
with urlopen(zipurl) as zipresp:
    with ZipFile(BytesIO(zipresp.read())) as zfile:
        zfile.extractall(final_directory)