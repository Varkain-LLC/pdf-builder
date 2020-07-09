import os
import json

import sys

sys.path.append('..')

from tools.html_to_pdf_converter import get_pdf_from_html
from jinja2 import Environment, FileSystemLoader

if len(sys.argv) != 4:
    print("usage: converter.py <json_source> <html_template_sourse> <filename_to_save>")
    exit()

# Used folders
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
assetsFolder = os.path.join(BASE_DIR, '../assets/')
driverFolder = assetsFolder + '/drivers/'

# The part where we get JSON data and create temp HTML file
# For details read the README file
file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)

template = env.get_template(sys.argv[2])

with open(assetsFolder + sys.argv[1]) as book:
    output = template.render(json_obj=json.loads(str(book.read())))

    # Write HTML String to temp.html
    with open("temp.html", "w") as file:
        file.write(output)

# The part where we get the new created temp.html and convert to PDF file
# For details read the README file
result = get_pdf_from_html('file://' + os.getcwd() + '/temp.html', chromedriver=driverFolder + 'chromedriver')
with open(assetsFolder + sys.argv[3], 'wb') as file:
    file.write(result)
    os.remove("temp.html")
