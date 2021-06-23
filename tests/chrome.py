from unittest.case import TestCase
import utils.chrome as utils
import os
# import argparse
from chrome_session import ChromeSession
from selenium import webdriver
import tracemalloc
from time import sleep

tracemalloc.start()

class TestChromeUtils(TestCase):

  # parser = argparse.ArgumentParser()
  # parser.add_argument('-cv', '--chrome_version')
  # args = parser.parse_args()

  chrome_version = '90'

  def test_get_chrome_version(self):
    actual = utils.get_chrome_version()
    if self.assertRegex(self.chrome_version, '\d*'):
      self.__class__.chrome_version = actual

  def test_download_chromedriver(self):
    self.assertTrue(utils.download_chromedriver(os.getcwd(), self.__class__.chrome_version))

  def test_get_chromedriver_version(self):
    self.assertRegex(utils.get_chromedriver_version(os.getcwd()), '\d*')
    self.assertEqual(utils.get_chromedriver_version(os.getcwd()), self.__class__.chrome_version)


class TestChromeSession(TestCase):
  
  def test_get_browser(self):
    session = ChromeSession()
    browser = session.get_browser()
    self.assertIsNotNone(browser)
    self.assertIsNotNone(session.session_id)
    self.assertIsNotNone(session.executor_url)
    self.assertIsInstance(browser, webdriver.Chrome)
    session.close()
    self.assertIsNone(session.browser)
    
  def test_profile_folder(self):
    session = ChromeSession(profile_folder=True)
    browser = session.get_browser()
    self.assertTrue(os.path.isdir('ChromeProfile'))

  def test_download_path(self):
    session = ChromeSession(download_path=os.getcwd())
    browser = session.get_browser()
    browser.get('http://speedtest.tele2.net/')
    browser.find_element_by_link_text('1MB').click()
    sleep(2)
    self.assertTrue(os.path.isfile('1MB.zip'))

  def test_add_pref(self):
    session = ChromeSession()
    session.add_pref('test', False)
    self.assertFalse(session.prefs['test'])

if __name__ == '__main__':
  # python -m unittest test.chrome.TestClass.test_method
  #
  unittest.main(verbosity=1)