import base64
import json
import platform

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


py_ver = platform.python_version()


def get_html_name(name):
    if py_ver.startswith('2'):
        return '{}.html'.format(name)
    return f'{name}.html'


def get_pdf_name(prefix, name):
    if py_ver.startswith('2'):
        return '{}{}.pdf'.format(prefix, name)
    return f'{prefix}{name}.pdf'


def send_devtools(driver, cmd, params={}):
    resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
    url = driver.command_executor._url + resource
    body = json.dumps({'cmd': cmd, 'params': params})
    response = driver.command_executor._request('POST', url, body)
    return response.get('value')


def get_pdf_from_html(path, chromedriver='./chromedriver', print_options={}):
    webdriver_options = Options()
    webdriver_options.add_argument('--headless')
    webdriver_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chromedriver, options=webdriver_options)

    driver.get(path)

    calculated_print_options = {
        'landscape': False,
        'displayHeaderFooter': False,
        'printBackground': True,
        'preferCSSPageSize': True,
    }
    calculated_print_options.update(print_options)
    result = send_devtools(driver, "Page.printToPDF", calculated_print_options)
    driver.quit()
    return base64.b64decode(result['data'])


if __name__ == "__main__":
    pass
