from unittest.case import TestCase
import utils.chrome as utils
from chrome_session import ChromeSession
from selenium import webdriver
import tracemalloc
from time import sleep

tracemalloc.start()


class TestRemote(TestCase):
  
  def test_remote_capture(self):
    session = ChromeSession()
    browser = session.get_browser()
    browser.get('https://www.google.com/')
    session_id = session.session_id
    executor_url = session.executor_url

    session2 = ChromeSession()
    remote_browser = session2.get_remote_browser(session_id, executor_url)

    self.assertTrue(remote_browser.find_element_by_xpath('*//img[@alt="Google"]'))


if __name__ == '__main__':
  # python -m unittest tests.chrome.TestClass.test_method
  #
  unittest.main(verbosity=1)