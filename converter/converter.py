import os
import json
import time

from tools.html_to_pdf_converter import get_pdf_from_html
from jinja2 import Environment, FileSystemLoader

# Used folders
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets/')


class HtmlToPdfConverter:
    """ The CLASS where we get JSON data and template
    create temp HTML file
    convert HTML to PDF
    For details read the README file
    """

    def __init__(self, template_vars, html_template_path):
        self.template_vars = template_vars
        self.html_template_path = html_template_path

    def create(self, output_file=None):
        file_loader = FileSystemLoader('templates')
        env = Environment(loader=file_loader)

        template = env.get_template(self.html_template_path)
        input_file = ASSETS_DIR + self.template_vars

        # Read JSON
        with open(input_file) as book:
            output = template.render(json_obj=json.loads(str(book.read())))
            # Write HTML String to temp.html
            with open("temp.html", "w") as file:
                file.write(output)

        # Temp to PDF
        result = get_pdf_from_html(
            path='file://' + os.getcwd() + '/temp.html',
            chromedriver=os.path.join(ASSETS_DIR, 'drivers/chromedriver')
        )

        if not output_file:
            output_file = str(int(time.time()))  # casting it first to int, in order to get rid of the milliseconds

        output_file = str(ASSETS_DIR) + str(output_file) + '.pdf'

        with open(output_file, 'wb') as file:
            file.write(result)
            os.remove('temp.html')


if __name__ == "__main__":
    html_to_pdf_obj = HtmlToPdfConverter(
        template_vars='book.json',
        html_template_path='book.html'
    )
    html_to_pdf_obj.create(
        output_file=''
    )
