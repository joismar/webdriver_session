import logging
from selenium import webdriver
from utils import *
import sys

class Session:
  '''Store a webdriver session
  '''
  def __init__(self, args=[]):
    self.webdriver = webdriver
    
    self.args = args
    self.log = logging.getLogger('session')
    self.log.level = logging.DEBUG
    stream_handler = logging.StreamHandler(sys.stdout)
    self.log.addHandler(stream_handler)

    self.browser = None
    self.session_id = None
    self.executor_url = None
      
  def get_browser(self):
    '''Configure and return a webdriver session

    :returns: A webdriver session
    '''
    self.setup_browser()

    self.session_id = self.browser.session_id
    self.executor_url = self.browser.command_executor._url

    self.log.info(f'Session started - ID: {self.session_id} EXECUTOR_URL: {self.executor_url}')

    return self.browser

  def close(self):
    self.browser.quit()
    self.browser = None
    self.log.info('Exited sucessffully.')
