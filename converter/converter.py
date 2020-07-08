import json
import os
import sys

sys.path.append('..')
from tools.html_to_pdf_converter import get_pdf_from_html

from jinja2 import Environment, FileSystemLoader

# The part where we get JSON data and create temp HTML file
# For details read the README file
file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)

template = env.get_template('book.html')

with open('../assets/book.json') as book:
    output = template.render(json_obj=json.loads(str(book.read())))

    # Write HTML String to temp.html
    with open("temp.html", "w") as file:
        file.write(output)

# The part where we get the new created temp.html and convert to PDF file
# For details read the README file
result = get_pdf_from_html('file://' + os.getcwd() + '/temp.html', chromedriver='../assets/drivers/chromedriver')
with open('../assets/book.pdf', 'wb') as file:
    file.write(result)
    os.remove("temp.html")
