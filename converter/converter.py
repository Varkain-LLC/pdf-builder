import os
import json
import time

from tools.html_to_pdf_converter import get_pdf_from_html
from jinja2 import Environment, FileSystemLoader, Template

# Used folders
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets/')


class HtmlToPdfConverter:
    """ The CLASS where we get JSON data and template
    create temp HTML file
    convert HTML to PDF
    For more details read the README file
    """

    def __init__(self, json_data=None, json_file_path=None, html_data=None, html_template_path=None):
        self.json_data = json_data
        self.json_file_path = json_file_path
        self.html_data = html_data
        self.html_template_path = html_template_path

    def get_template_instance(self, json_file=None):
        """Get template by path"""
        file_loader = FileSystemLoader('templates')
        env = Environment(loader=file_loader)

        if json_file:
            return env.get_template(self.html_template_path).render(json_obj=json.loads(str(json_file.read())))
        else:
            return env.get_template(self.html_template_path).render(json_obj=self.json_data)

    def write_temp_html_file(self):
        """
        Write rendered template to temp.html
        """
        if self.json_file_path:
            json_file_path = os.path.join(ASSETS_DIR, self.json_file_path)
            try:
                with open(os.path.abspath(json_file_path)) as json_file:
                    try:
                        if self.html_template_path:
                            output = self.get_template_instance(json_file)
                        else:
                            output = Template(self.html_data).render(json_obj=json.loads(str(json_file.read())))
                    except IOError:
                        raise Exception('Could not read file')
            except FileNotFoundError:
                print('No file')
                exit()
        else:
            if self.html_template_path:
                output = self.get_template_instance()
            else:
                output = Template(self.html_data).render(json_obj=self.json_data)
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
        # json_file_path='book.json',
        json_data={
            "name": "qqqq",
            "description": "wwww",
            "price": 123
        },
        # html_template_path='book.html',
        html_data='<div class="container"><div class="row"><div class="col-lg-12 text-center">'
                  '<h1 class="mt-5">{{ json_obj.name }}</h1><p class="lead">{{ json_obj.description }}</p>'
                  '<p class="lead">{{ json_obj.price }}</p></div></div></div>'
    )
    html_to_pdf_obj.create(
        output_file=''
    )
