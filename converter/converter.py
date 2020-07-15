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

    def __init__(self, json_data, html_template_path):
        self.json_data = json_data
        self.html_template_path = html_template_path

    def get_template(self):
        """Get template by path"""
        file_loader = FileSystemLoader('templates')
        env = Environment(loader=file_loader)

        return env.get_template(self.html_template_path)

    def write_temp_html_file(self):
        """
        Write rendered template to temp.html
        """
        if isinstance(self.json_data, str):
            json_data_file_path = os.path.join(ASSETS_DIR, self.json_data)
            try:
                with open(os.path.abspath(json_data_file_path)) as book:
                    try:
                        output = self.get_template().render(json_obj=json.loads(str(book.read())))
                    except IOError:
                        print('Could not read file')
                        exit()
            except FileNotFoundError:
                print('No file')
                exit()
        else:
            output = self.get_template().render(json_obj=self.json_data)

        try:
            with open("temp.html", "w") as file:
                try:
                    file.write(output)  # Write HTML String to temp.html
                except IOError:
                    print('Could not open temp.html file')
                    exit()
        except FileNotFoundError:
            print('No file')
            exit()

    @staticmethod
    def get_pdf_file():
        """Get pdf file"""
        return get_pdf_from_html(
            path='file://' + os.getcwd() + '/temp.html',
            chromedriver=os.path.join(ASSETS_DIR, 'drivers/chromedriver')
        )

    def write_pdf_file(self, output_file):
        try:
            with open(output_file, 'wb') as file:
                try:
                    file.write(self.get_pdf_file())
                    os.remove('temp.html')
                except IOError:
                    print('Could not write pdf file')
                    exit()
        except FileNotFoundError:
            print('No file')
            exit()

    def create(self, output_file=None):
        self.write_temp_html_file()

        if not output_file:
            output_file = str(int(time.time()))  # casting it first to int, in order to get rid of the milliseconds
        output_file = f'{ASSETS_DIR}{output_file}.pdf'

        if os.path.isfile('./temp.html'):
            self.write_pdf_file(output_file=output_file)


if __name__ == "__main__":
    html_to_pdf_obj = HtmlToPdfConverter(
        # json_data='book.json',
        json_data={
            "name": "qqqq",
            "description": "wwww",
            "price": 123
        },
        html_template_path='book.html'
    )
    html_to_pdf_obj.create(
        output_file=''
    )
