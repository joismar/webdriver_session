import selenium
from utils.logger import Logger
from selenium import webdriver
from utils import *
import sys

class Session:
  '''Store a webdriver session
  '''
  def __init__(self):
    self.webdriver = webdriver

    self.log = Logger('session').log

    self.browser = None
    self.session_id = None
    self.executor_url = None

  
  def get_browser(self) -> webdriver.Remote:
    '''Configure and return a webdriver session

    :returns: A webdriver session
    '''
    try:
      self.browser = self.setup_browser()
    except AttributeError as e:
      self.log.error(e)
      self.log.warning('Method setup_browser should be implemented.')

    self.session_id = self.browser.session_id
    self.executor_url = self.browser.command_executor._url

    self.log.info(f'Session started - ID: {self.session_id} EXECUTOR_URL: {self.executor_url}')

    return self.browser

  def get_remote_browser(self, session_id, executor_url) -> webdriver.Remote:
    pass

  def close(self):
    self.browser.quit()
    self.browser = None
    self.log.info('Exited sucessffully.')


  def __delattr__(self):
    Logger('session').destroy()

