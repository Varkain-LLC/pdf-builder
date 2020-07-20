import os
import json
import string
import time

import secrets
import numpy as np
from functools import partial

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

    def produce_amount_names(self, amount_of_names, _randint=np.random.randint):
        names = set()
        pickchar = partial(secrets.choice, string.ascii_lowercase + string.digits)
        while len(names) < amount_of_names:
            names |= {''.join([pickchar() for _ in range(_randint(12, 20))]) for _ in
                      range(amount_of_names - len(names))}
        return names

    def get_json(self):
        if self.json_file_path:
            json_file_path = os.path.join(ASSETS_DIR, self.json_file_path)
            with open(os.path.abspath(json_file_path)) as json_file:
                return json.loads(str(json_file.read()))
        return self.json_data

    def render_template(self, json_data=None):
        """Get template by path"""
        file_loader = FileSystemLoader('templates')
        env = Environment(loader=file_loader)
        if self.html_template_path:
            return env.get_template(self.html_template_path).render(json_obj=json_data)
        else:
            return Template(self.html_data).render(json_obj=json_data)

    def create_temp_html_file(self, rendered_html=None):
        """
        Write rendered template to temp html
        """
        with open(f'{list(self.produce_amount_names(1))[0]}.html', "w") as file:
            file.write(rendered_html)  # Write HTML String to temp html
            return file.name

    @staticmethod
    def get_pdf_file(temp_html_file_path):
        """Get pdf file"""
        return get_pdf_from_html(
            path='file://' + os.getcwd() + str('/' + temp_html_file_path),
            chromedriver=os.path.join(ASSETS_DIR, 'drivers/chromedriver')
        )

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
            output_file = list(self.produce_amount_names(1))[0]  # using function for generate random name
        output_file = f'{ASSETS_DIR}{output_file}.pdf'

        if os.path.isfile(str('./' + temp_html_file_path)):
            self.write_pdf_file(
                temp_html_file_path=temp_html_file_path,
                output_file=output_file
            )

        return output_file


if __name__ == "__main__":
    html_to_pdf_obj = HtmlToPdfConverter(
        json_file_path='book.json',
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
