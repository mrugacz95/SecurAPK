import os.path
import shutil
import subprocess
import requests

APKTOOL_PATH = 'apktool.jar'

if not os.path.isfile(APKTOOL_PATH):
    r = requests.get('https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.3.1.jar')
    if r.status_code == 200:
        with open(APKTOOL_PATH, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)



def decompile(file_path):
    subprocess.call(args=['apktool','d',file_path]) #TODO implement
