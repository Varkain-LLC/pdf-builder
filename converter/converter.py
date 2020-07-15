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

    def get_json(self):
        if self.json_file_path:
            json_file_path = os.path.join(ASSETS_DIR, self.json_file_path)
            try:
                with open(os.path.abspath(json_file_path)) as json_file:
                    return json.loads(str(json_file.read()))
            except FileNotFoundError:
                print('No file')
                exit()
        return self.json_data

    def render_template(self, json_data=None):
        """Get template by path"""
        file_loader = FileSystemLoader('templates')
        env = Environment(loader=file_loader)
        if self.html_template_path:
            return env.get_template(self.html_template_path).render(json_obj=json_data)
        else:
            return Template(self.html_data).render(json_obj=json_data)

    @staticmethod
    def create_temp_html_file(rendered_html=None):
        """
        Write rendered template to temp.html
        """
        try:
            with open("temp.html", "w") as file:
                try:
                    file.write(rendered_html)  # Write HTML String to temp.html
                    return file.name
                    # return file.name
                except IOError:
                    print('Could not open temp.html file')
                    exit()
        except FileNotFoundError:
            print('No file')
            exit()

    @staticmethod
    def get_pdf_file(temp_html_file_path):
        """Get pdf file"""
        return get_pdf_from_html(
            path='file://' + os.getcwd() + temp_html_file_path,
            chromedriver=os.path.join(ASSETS_DIR, 'drivers/chromedriver')
        )

    def write_pdf_file(self, temp_html_file_path, output_file):
        try:
            with open(output_file, 'wb') as file:
                try:
                    file.write(self.get_pdf_file(temp_html_file_path))
                    os.remove(temp_html_file_path)
                except IOError:
                    print('Could not write pdf file')
                    exit()
        except FileNotFoundError:
            print('No file')
            exit()

    def create(self, output_file=None):
        json_data = self.get_json()
        rendered_html = self.render_template(json_data)

        temp_html_file_path = self.create_temp_html_file(rendered_html)

        if not output_file:
            output_file = str(int(time.time()))  # casting it first to int, in order to get rid of the milliseconds
        output_file = f'{ASSETS_DIR}{output_file}.pdf'

        if os.path.isfile(str('./'+temp_html_file_path)):
            self.write_pdf_file(
                temp_html_file_path=temp_html_file_path,
                output_file=output_file
            )

        return output_file


if __name__ == "__main__":
    html_to_pdf_obj = HtmlToPdfConverter(
        # json_file_path='book.json',
        json_data={
            "name": "qqqq",
            "description": "wwww",
            "price": 123
        },
        html_template_path='book.html',
        html_data='<div class="container"><div class="row"><div class="col-lg-12 text-center">'
                  '<h1 class="mt-5">{{ json_obj.name }}</h1><p class="lead">{{ json_obj.description }}</p>'
                  '<p class="lead">{{ json_obj.price }}</p></div></div></div>'
    )
    html_to_pdf_obj.create(
        output_file=''
    )
