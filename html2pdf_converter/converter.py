# coding: utf-8
import os
import json
import sys
import platform

# from jinja2 import Environment, FileSystemLoader
from jinja2 import Template

from tools.html_to_pdf_converter import (
    get_pdf_from_html,
    get_html_name,
    get_pdf_name,
)
from tools.random_names import produce_amount_names

from choices import templates


is_python2 = platform.python_version().startswith('2.7')


class HtmlToPdfConverter:
    """
    The CLASS where we get JSON data and template
    create temp HTML file
    convert HTML to PDF
    For more details read the README file
    """

    def __init__(
        self,
        base_dir=None,
        json_data=None, html_data=None,
        json_file_path=None, html_template_path=None
    ):
        self.json_data = json_data
        self.json_file_path = json_file_path
        self.html_data = html_data
        self.html_template_path = html_template_path
        self.base_dir = base_dir or os.path.abspath(os.path.join(
            os.path.dirname(os.path.dirname(__file__)), '..'))
        self.assets_dir = os.path.join(self.base_dir, 'assets/')
        self.static_url = os.path.join(self.base_dir, 'static/')
        self.chromium_path = os.path.join(self.assets_dir, 'drivers/')

    def get_chromium_driver(self):
        _type = sys.platform
        if _type in ('linux', 'linux2'):
            return os.path.join(self.chromium_path, 'linux-chromedriver')

        if _type == 'darwin':
            return os.path.join(self.chromium_path, 'mac-chromedriver')

        if _type == 'win32':
            return os.path.join(self.chromium_path, 'chromedriver.exe')

    def get_json(self):
        if self.json_file_path:
            with open(os.path.abspath(self.json_file_path)) as json_file:
                return json.loads(str(json_file.read()))
        return json.loads((self.json_data))

    def render_template(self, json_data=None):
        """Get template by path"""
        # file_loader = FileSystemLoader('templates')
        # env = Environment(loader=file_loader)
        if self.html_template_path:
            # return env.get_template(self.html_template_path).render(
            #     json_obj=json_data)
            _path = os.path.join(
                self.base_dir,
                'templates',
                self.html_template_path
            )
            with open(os.path.abspath(_path)) as html_file:
                self.html_data = html_file.read()

        if is_python2:
            self.html_data = self.html_data.decode('utf-8')

        return Template(self.html_data).render(
            json_obj=json_data,
            static_url=self.static_url
        )

    @staticmethod
    def create_temp_html_file(rendered_html=None):
        """
        Write rendered template to temp html
        """
        if is_python2:
            rendered_html = rendered_html.encode('utf-8')

        _name = get_html_name(list(produce_amount_names(1))[0])
        with open(_name, "w") as file:
            file.write(rendered_html)  # Write HTML String to temp html
            return file.name

    def get_pdf_file(self, temp_html_file_path, output_file=None):
        """Get pdf file"""
        html_path = 'file://' + os.getcwd() + str('/' + temp_html_file_path)
        return get_pdf_from_html(
            path=html_path, chromedriver=self.get_chromium_driver(),
            pdf_file_path=output_file)

    def write_pdf_file(self, temp_html_file_path, output_file):
        with open(output_file, 'wb') as file:
            file.write(self.get_pdf_file(temp_html_file_path))
            os.remove(temp_html_file_path)
            # print(temp_html_file_path)

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
            output_file = get_pdf_name(self.assets_dir, output_file)

        if os.path.isfile(str('./' + temp_html_file_path)):
            if output_file:
                self.get_pdf_file(temp_html_file_path, output_file)
            else:
                self.write_pdf_file(
                    temp_html_file_path=temp_html_file_path,
                    output_file=output_file
                )

        return output_file


if __name__ == "__main__":
    html_to_pdf_obj = HtmlToPdfConverter(
        json_file_path=sys.argv[1],  # 'assets/book.json'
        json_data=json.dumps({
            "name": "qqqq",
            "description": "wwww",
            "price": 123
        }),
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
