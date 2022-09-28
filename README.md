# Webdriver Session

This package is intended to help the developer with webdriver instances, such as downloading updates automatically, session settings and remote instances.

## Installation

```sh
# execute in root path of project
python -m pip install .
# FROM GIT
pip install --upgrade git+https://github.com/joismar/webdriver_session.git
```

## Usage example

```python
from webdriver_session import ChromeSession

session = ChromeSession(
  profile_folder=False, # True if you want to generate profile folder inside the project folder and persist it
  download_path=None, # path for files downloaded in browser
  driver=None, # if you want to specify a custom webdriver class
  args=[], # if you want pass browser args, equivalent to options<ChromeOptions>.add_argument('--argument_here')
)

# get a new browser, a webdriver file will download automatically
browser = session.get_browser()

browser.get('https://google.com')
```

## Development setup

Describe how to install all development dependencies and how to run an automated test-suite of some kind. Potentially do this for multiple platforms.

```sh
poetry install
poetry shell
python -m pip install -e .
```

### Tests
```sh
# before development setup described above
python -m unittest <tests-path> # see tests for more informations
```

## Release History

* 0.2.0
    * Second dev release, with build support.
    * Webdriver Remote Session support.
* 0.1.0
    * First dev reselase, with base classes.

## Meta

Joismar Braga – cloudwilker@gmail.com

Distributed under the MIT license. See ``LICENSE`` for more information.

[https://github.com/joismar/webdriver_session](https://github.com/joismar/webdriver_session)

## Contributing

1. Fork it (<https://github.com/joismar/webdriver_session/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
