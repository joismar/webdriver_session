import logging
import os
import re
import requests
from glob import glob
from zipfile import ZipFile
from win32api import HIWORD, GetFileVersionInfo
import wget

log = logging.getLogger()

def download_chromedriver(chromedriver_path, chrome_version):
  try:
    latest = requests.get(f'https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{chrome_version}')
    wget.download(f'https://chromedriver.storage.googleapis.com/{latest.text}/chromedriver_win32.zip', f'{chromedriver_path}\\chromedriver_win32.zip')

    with ZipFile('{}\\chromedriver_win32.zip'.format(chromedriver_path), 'r') as zip_ref:
      zip_ref.extractall(chromedriver_path)
      
    os.remove(f'{chromedriver_path}\\chromedriver_win32.zip')
        
    if os.path.exists(f'{chromedriver_path}\\chromedriver.exe'):
      return True
    else: 
      return False
  except Exception as e:
    log.error(e)
    return False
    
def get_chromedriver_version(chromedriver_path):
  stream = os.popen('{}\\chromedriver.exe --version'.format(chromedriver_path))
  output = stream.read()
  chromedriver_version = re.search('\d*\.\d*\.\d*\.\d*', output).group().split('.')[0]
  stream.close()

  return chromedriver_version

def get_chrome_version():
  path = glob('C:\Program *\Google\Chrome\Application\chrome.exe')

  if not path: 
    raise FileNotFoundError("Google Chrome installation don't found")
  info = GetFileVersionInfo(path[0], "\\")
  ms = info['FileVersionMS']
  
  return str(HIWORD(ms))
