import base64
import json
import subprocess
import sys

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


def get_pdf_from_html_terminal(path, pdf_file_path):
    if sys.version_info[0] == 2:
        return subprocess.call([
            "/opt/google/chrome/chrome",
            "--no-sandbox",
            "--headless",
            "--disable-gpu",
            "--disable-dev-shm-usage",
            "--print-to-pdf={}".format(pdf_file_path),
            path,
        ])
    return subprocess.run([
        "/opt/google/chrome/chrome",
        "--no-sandbox",
        "--headless",
        "--disable-gpu",
        "--disable-dev-shm-usage",
        "--print-to-pdf={}".format(pdf_file_path),
        path,
    ], stdout=subprocess.DEVNULL)


def get_pdf_from_html(
    path, chromedriver='./chromedriver', print_options={},
    pdf_file_path=None
):
    if pdf_file_path:
        return get_pdf_from_html_terminal(path, pdf_file_path)
    webdriver_options = Options()
    webdriver_options.add_argument('--timeout {timeout}'.format(
        timeout=5*60*1000))  # 5 minutes
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
