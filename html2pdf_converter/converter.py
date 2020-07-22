import os
import json
import sys

from jinja2 import Environment, FileSystemLoader, Template

from tools.html_to_pdf_converter import get_pdf_from_html
from tools.random_names import produce_amount_names

from choices import templates

# Used folders
BASE_DIR = os.path.abspath(os.path.join(
    os.path.dirname(os.path.dirname(__file__)), '..'))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets/')
CHROMIUM_PATH = os.path.join(ASSETS_DIR, 'drivers/')


def get_chromium_driver():
    _type = sys.platform
    if _type in ('linux', 'linux2'):
        return os.path.join(CHROMIUM_PATH, 'linux-chromedriver')

    if _type == 'darwin':
        return os.path.join(CHROMIUM_PATH, 'mac-chromedriver')

    if _type == 'win32':
        return os.path.join(CHROMIUM_PATH, 'chromedriver.exe')


class HtmlToPdfConverter:
    """
    The CLASS where we get JSON data and template
    create temp HTML file
    convert HTML to PDF
    For more details read the README file
    """

    def __init__(
        self, json_data=None, html_data=None,
        json_file_path=None, html_template_path=None
    ):
        self.json_data = json_data
        self.json_file_path = json_file_path
        self.html_data = html_data
        self.html_template_path = html_template_path

    def get_json(self):
        if self.json_file_path:
            with open(os.path.abspath(self.json_file_path)) as json_file:
                return json.loads(str(json_file.read()))
        return self.json_data

    def render_template(self, json_data=None):
        """Get template by path"""
        file_loader = FileSystemLoader('templates')
        env = Environment(loader=file_loader)
        if self.html_template_path:
            return env.get_template(self.html_template_path).render(
                json_obj=json_data)
        else:
            return Template(self.html_data).render(json_obj=json_data)

    @staticmethod
    def create_temp_html_file(rendered_html=None):
        """
        Write rendered template to temp html
        """
        with open(f'{list(produce_amount_names(1))[0]}.html', "w") as file:
            file.write(rendered_html)  # Write HTML String to temp html
            return file.name

    @staticmethod
    def get_pdf_file(temp_html_file_path):
        """Get pdf file"""
        html_path = 'file://' + os.getcwd() + str('/' + temp_html_file_path)
        return get_pdf_from_html(
            path=html_path, chromedriver=get_chromium_driver())

    def write_pdf_file(self, temp_html_file_path, output_file):
        with open(output_file, 'wb') as file:
            file.write(self.get_pdf_file(temp_html_file_path))
            os.remove(temp_html_file_path)

    def get_html(self):
        json_data = self.get_json()
        rendered_html = self.render_template(json_data)

        return rendered_html

    def create(self, output_file=None):
        html = self.get_html()
        temp_html_file_path = self.create_temp_html_file(html)

        if not output_file:
            # using function for generate random name
            output_file = list(produce_amount_names(1))[0]
            output_file = f'{ASSETS_DIR}{output_file}.pdf'

        if os.path.isfile(str('./' + temp_html_file_path)):
            self.write_pdf_file(
                temp_html_file_path=temp_html_file_path,
                output_file=output_file
            )

        return output_file


if __name__ == "__main__":
    html_to_pdf_obj = HtmlToPdfConverter(
        json_file_path=sys.argv[1],  # 'assets/book.json'
        json_data={
            "name": "qqqq",
            "description": "wwww",
            "price": 123
        },
        html_template_path=templates.get(sys.argv[2]),
        html_data='<div class="container">'
        '<div class="row"><div class="col-lg-12 text-center">'
        '<h1 class="mt-5">{{ json_obj.name }}</h1>'
        '<p class="lead">{{ json_obj.description }}</p>'
        '<p class="lead">{{ json_obj.price }}</p></div></div></div>'
    )
    html_to_pdf_obj.create(
        output_file=sys.argv[3]
    )
