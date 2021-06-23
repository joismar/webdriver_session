from time import sleep
from selenium import webdriver
from utils.chrome import *
from session import Session
import os

class ChromeSession(Session):
  '''Store a webdriver.Chrome session

  :param profile_folder: <string> of a path profile folder location
  :param download_path:
  :param driver: A custom <webdriver.Chrome>. If passed, overrides default webdriver.Chrome class
  :param options: A <list> of strings of chromedriver options arguments
  '''

  def __init__(
      self,
      profile_folder=False,
      download_path=None,
      driver=None,
      args=[]
    ):

    Session.__init__(self)

    self.args = args
    self.chrome = driver or webdriver.Chrome 
    self.download_path = download_path or os.getcwd()
    self.chromedriver_path = os.path.dirname(__file__)
    self.prefs = {
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "download.default_directory": self.download_path
    }
    self.session_id = None
    self.executor_url = None
    self.chrome_version = get_chrome_version()
    self.chromedriver_version = None

    self.profile_folder = f'{os.getcwd()}/ChromeProfile' if profile_folder else profile_folder

      
  def add_pref(self, key, value):
    '''Receive a key:pair and add to prefs dict

    :param key: <string> of key
    :param value: <string> of value
    '''
    if self.session_id:
      return self.log.warning('Session already started.')
    
    self.prefs[key] = value 


  def setup_browser(self) -> webdriver.Chrome:
    '''Perform webdriver setup
    '''
    updated = False
    downloaded = False

    while True:
      if os.path.exists(f'{self.chromedriver_path}\\chromedriver.exe'):
        downloaded = True
        self.chromedriver_version = get_chromedriver_version(self.chromedriver_path)
        self.chrome_version = get_chrome_version()
        
        if int(self.chromedriver_version) != int(self.chrome_version):
          self.log.info('Updating chromedriver...')
              
          download_chromedriver(self.chromedriver_path, self.chrome_version)

          self.chromedriver_version = get_chromedriver_version(self.chromedriver_path)
          self.chrome_version = self.get_chrome_version()

          updated = int(self.chromedriver_version) == int(self.chrome_version)

        else:
          updated = True
          
      else: 
        self.log.info('chromedriver.exe not found. Downloading...')
        downloaded = download_chromedriver(self.chromedriver_path, self.chrome_version)
          
      if not downloaded: continue

      if updated:
        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", self.prefs)

        for arg in self.args:
            options.add_argument(arg)
        
        if self.profile_folder:
          if not os.path.exists(self.profile_folder):
            os.makedirs(self.profile_folder)
              
          options.add_argument(f'user-data-dir={self.profile_folder}')
            
        options.add_argument('--start-maximized')
        
        browser = self.chrome('{}\\chromedriver.exe'.format(self.chromedriver_path), options=options)
        log.info(browser)
        return browser

      else:
        sleep(3)
        continue
