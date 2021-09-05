from unittest.case import TestCase
from unittest import main
from webdriver_session import ChromeSession
import tracemalloc
from time import sleep

tracemalloc.start()


# python -m unittest tests.remote.TestRemote
class TestRemote(TestCase):

    # python -m unittest tests.remote.TestRemote.test_remote_capture
    def test_remote_capture(self):
        session = ChromeSession()
        browser = session.get_browser()
        browser.get('https://www.google.com/')
        session_id = session.session_id
        executor_url = session.executor_url

        session2 = ChromeSession()
        remote_browser = session2.get_remote_browser(session_id, executor_url)

        self.assertTrue(remote_browser.find_element_by_xpath(
            '*//input[@type="text"]'))

        session.close()
        session2.close()


if __name__ == '__main__':
    main(verbosity=1)
