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

    def __init__(self, json_file_path, html_template_path):
        self.json_file_path = json_file_path
        self.html_template_path = html_template_path

    def get_template(self):
        """Get template by path"""
        file_loader = FileSystemLoader('templates')
        env = Environment(loader=file_loader)

        return env.get_template(self.html_template_path)

    def get_html_file(self):
        """Get html file by path"""
        input_file = ASSETS_DIR + self.json_file_path

        return input_file

    @staticmethod
    def get_pdf_file():
        """Get pdf file"""
        return get_pdf_from_html(
            path='file://' + os.getcwd() + '/temp.html',
            chromedriver=os.path.join(ASSETS_DIR, 'drivers/chromedriver')
        )

    def create(self, output_file=None):
        """
        Write rendered template to temp.html
        Convert temp.html to pdf
        """
        with open(self.get_html_file()) as book:
            output = self.get_template().render(json_obj=json.loads(str(book.read())))
            with open("temp.html", "w") as file:
                file.write(output)  # Write HTML String to temp.html

        if not output_file:
            output_file = str(int(time.time()))  # casting it first to int, in order to get rid of the milliseconds
        output_file = str(ASSETS_DIR) + str(output_file) + '.pdf'

        with open(output_file, 'wb') as file:
            file.write(self.get_pdf_file())
            os.remove('temp.html')


if __name__ == "__main__":
    html_to_pdf_obj = HtmlToPdfConverter(
        json_file_path='book.json',
        html_template_path='book.html'
    )
    html_to_pdf_obj.create(
        output_file=''
    )
