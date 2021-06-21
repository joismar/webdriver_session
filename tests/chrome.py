import unittest
from unittest.case import TestCase
import utils.chrome as utils
import os
# import argparse
from session import WebdriverSession
from selenium import webdriver
import tracemalloc

tracemalloc.start()

class TestChromeUtils(unittest.TestCase):

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


class TestChromeSession(unittest.TestCase):

  session = WebdriverSession()
  
  def test_setup_browser(self):
    session = self.__class__.session
    session.setup_browser()
    self.assertIsNotNone(session.browser)
    self.assertIsInstance(session.browser, webdriver.Chrome)
    session.close()
    self.assertIsNone(session.browser)
  
  def test_get_browser(self):
    session = self.__class__.session
    browser = session.get_browser()
    self.assertIsNotNone(browser)
    self.assertIsNotNone(session.session_id)
    self.assertIsNotNone(session.executor_url)
    self.assertIsInstance(browser, webdriver.Chrome)
    session.close()
    self.assertIsNone(session.browser)


if __name__ == '__main__':
    unittest.main(verbosity=1)