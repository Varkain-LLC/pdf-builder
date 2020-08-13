import base64
import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_html_name(name):
    # support python2.7
    return '{}.html'.format(name)


def get_pdf_name(prefix, name):
    # support python2.7
    return '{}{}.pdf'.format(prefix, name)


def send_devtools(driver, cmd, params={}):
    resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
    url = driver.command_executor._url + resource
    body = json.dumps({'cmd': cmd, 'params': params})
    response = driver.command_executor._request('POST', url, body)
    return response.get('value')


def get_pdf_from_html(path, chromedriver='./chromedriver', print_options={}):
    webdriver_options = Options()
    timeout = 5*60*1000  # 5 minutes
    webdriver_options.add_argument(f'--timeout {timeout}')  # 5 minutes
    webdriver_options.add_argument('--headless')
    webdriver_options.add_argument('--disable-gpu')
    webdriver_options.add_argument('--no-sandbox')
    webdriver_options.add_argument('--disable-dev-shm-usage')
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
