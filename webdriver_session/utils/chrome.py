import logging
import os
import re
import requests
import shutil
from subprocess import run
from zipfile import ZipFile
import wget

log = logging.getLogger()


def download_chromedriver(chromedriver_path, chrome_version):
    if chrome_version <= '115':
        try:
            latest = requests.get(
                f'https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{chrome_version}')
            wget.download(
                f'https://chromedriver.storage.googleapis.com/{latest.text}/chromedriver_win32.zip', f'{chromedriver_path}\\chromedriver_win32.zip')

            with ZipFile('{}\\chromedriver_win32.zip'.format(chromedriver_path), 'r') as zip_ref:
                zip_ref.extractall(chromedriver_path)

            os.remove(f'{chromedriver_path}\\chromedriver_win32.zip')

            if os.path.exists(f'{chromedriver_path}\\chromedriver.exe'):
                return True
            else:
                return False
        except Exception as e:
            log.error(e)
            return False

    try:
        latest = requests.get(
            f'https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_{chrome_version}')
        wget.download(
	        f'https://storage.googleapis.com/chrome-for-testing-public/{latest.text}/win32/chromedriver-win32.zip',  f'{chromedriver_path}\\chromedriver_win32.zip')
        with ZipFile(fr'{chromedriver_path}\\chromedriver_win32.zip') as zip_ref:
            zip_ref.extractall(chromedriver_path)

        src = os.path.join(chromedriver_path, 'chromedriver-win32', 'chromedriver.exe')
        dst = os.path.join(chromedriver_path, 'chromedriver.exe')
        shutil.move(src, dst)
        shutil.rmtree(os.path.join(chromedriver_path, 'chromedriver-win32'))
        os.remove(f'{chromedriver_path}\\chromedriver_win32.zip')

        if os.path.exists(f'{chromedriver_path}\\chromedriver.exe'):
            return True
        else:
            return False
    except Exception as e:
        log.error(e)
        return False


def get_chromedriver_version(chromedriver_path):
    stream = os.popen(
        '{}\\chromedriver.exe --version'.format(chromedriver_path))
    output = stream.read()
    chromedriver_version = re.search(
        r'\d*\.\d*\.\d*\.\d*', output).group().split('.')[0]
    stream.close()

    return chromedriver_version


def get_chrome_version():
    try:
        p32 = run(
            [
                'powershell',
                '-Command',
                '''Get-ChildItem -Path "HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall" |
                Where {$_.GetValue("DisplayName") -match "Google Chrome"} |
                Get-ItemProperty |
                select -ExpandProperty DisplayVersion'''
            ], capture_output=True
        ).stdout
        p64 = run(
            [
                'powershell',
                '-Command',
                '''Get-ChildItem -Path "HKLM:\\SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall" |
                Where {$_.GetValue("DisplayName") -match "Google Chrome"} |
                Get-ItemProperty |
                select -ExpandProperty DisplayVersion'''
            ], capture_output=True
        ).stdout
    except Exception as e:
        log.error(e)
        raise

    if p32 and p64:
        log.warning('Multiple Chrome versions are installed, please uninstall one.')

    output = ''

    if p32: output = p32.decode('utf-8')
    if p64: output = p64.decode('utf-8')

    if output:
        return output.split('.')[0]
