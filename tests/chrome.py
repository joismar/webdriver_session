from unittest.case import TestCase
from unittest import main
import webdriver_session.utils.chrome as utils
import os
from webdriver_session import ChromeSession
from selenium import webdriver
import tracemalloc
from time import sleep

tracemalloc.start()


# python -m unittest tests.chrome.TestChromeUtils
class TestChromeUtils(TestCase):

    chrome_version = '93'

    # python -m unittest tests.chrome.TestChromeUtils.test_get_chrome_version
    def test_get_chrome_version(self):
        actual = utils.get_chrome_version()
        self.assertRegex(self.chrome_version, '\d*')
        self.assertTrue(self.__class__.chrome_version == actual)

    # python -m unittest tests.chrome.TestChromeUtils.test_download_chromedriver
    def test_download_chromedriver(self):
        self.assertTrue(utils.download_chromedriver(
            os.getcwd(), self.__class__.chrome_version))

    # python -m unittest tests.chrome.TestChromeUtils.test_get_chromedriver_version
    def test_get_chromedriver_version(self):
        self.assertRegex(utils.get_chromedriver_version(os.getcwd()), '\d*')
        self.assertEqual(utils.get_chromedriver_version(
            os.getcwd()), self.__class__.chrome_version)


# python -m unittest tests.chrome.TestChromeSession
class TestChromeSession(TestCase):
    # python -m unittest tests.chrome.TestChromeSession.test_get_browser
    def test_get_browser(self):
        session = ChromeSession()
        browser = session.get_browser()
        self.assertIsNotNone(browser)
        self.assertIsNotNone(session.session_id)
        self.assertIsNotNone(session.executor_url)
        self.assertIsInstance(browser, webdriver.Chrome)
        session.close()
        self.assertIsNone(session.browser)

    # python -m unittest tests.chrome.TestChromeSession.test_profile_folder
    def test_profile_folder(self):
        session = ChromeSession(profile_folder=True)
        session.get_browser()
        self.assertTrue(os.path.isdir('ChromeProfile'))

    # python -m unittest tests.chrome.TestChromeSession.test_download_path
    def test_download_path(self):
        session = ChromeSession(download_path=os.getcwd())
        browser = session.get_browser()
        browser.get('http://speedtest.tele2.net/')
        browser.find_element_by_link_text('1MB').click()
        sleep(2)
        self.assertTrue(os.path.isfile('1MB.zip'))

    # python -m unittest tests.chrome.TestChromeSession.test_add_pref
    def test_add_pref(self):
        session = ChromeSession()
        session.add_pref('test', False)
        self.assertFalse(session.prefs['test'])


if __name__ == '__main__':
    main(verbosity=1)
