from .utils.logger import Logger
from selenium import webdriver


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
            return False

        self.session_id = self.browser.session_id
        self.executor_url = self.browser.command_executor._url

        self.log.info(
            f'Session started - ID: {self.session_id} EXECUTOR_URL: {self.executor_url}')

        return self.browser

    def get_remote_browser(self, session_id, executor_url) -> webdriver.Remote:
        # Code by tarunlalwani@GitHub

        from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver

        # Save the original function, so we can revert our patch
        org_command_execute = RemoteWebDriver.execute

        def new_command_execute(self, command, params=None):
            if command == "newSession":
                # Mock the response
                return {'success': 0, 'value': None, 'sessionId': session_id}
            else:
                return org_command_execute(self, command, params)

        # Patch the function before creating the driver object
        RemoteWebDriver.execute = new_command_execute

        new_driver = webdriver.Remote(
            command_executor=executor_url, desired_capabilities={})
        new_driver.session_id = session_id

        # Replace the patched function with original function
        RemoteWebDriver.execute = org_command_execute

        self.browser = new_driver
        self.session_id = self.browser.session_id
        self.executor_url = self.browser.command_executor._url

        return self.browser

    def close(self):
        self.browser.quit()
        self.browser = None
        self.log.info('Exited sucessffully.')

    def __delattr__(self):
        Logger('session').destroy()
