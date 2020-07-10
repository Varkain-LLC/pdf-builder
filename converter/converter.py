import os
import json
import time

from tools.html_to_pdf_converter import get_pdf_from_html
from jinja2 import Environment, FileSystemLoader

# Used folders
assetsFolder = '../assets/'
driverPath = assetsFolder + '/drivers/chromedriver'


# The CLASS where we get JSON data and template
# create temp HTML file
# convert HTML to PDF
# For details read the README file
class HtmlToPdfConverter:
    def __init__(self, template_vars, html_template):
        print(f'Initializing {template_vars}, {html_template}')
        self.template_vars = template_vars
        self.html_template = html_template

    def create(self, output_file=None):
        file_loader = FileSystemLoader('templates')
        env = Environment(loader=file_loader)
        template = env.get_template(self.html_template)
        input_file = assetsFolder + self.template_vars

        # Read JSON
        with open(input_file) as book:
            print('Rendering template')
            output = template.render(json_obj=json.loads(str(book.read())))
            # Write HTML String to temp.html
            with open("temp.html", "w") as file:
                file.write(output)

        # Temp to PDF
        result = get_pdf_from_html(
            path='file://' + os.getcwd() + '/temp.html',
            chromedriver=driverPath
        )

        if not output_file:
            output_file = str(int(time.time()))  # casting it first to int, in order to get rid of the milliseconds

        output_file = str(assetsFolder) + str(output_file) + '.pdf'

        with open(output_file, 'wb') as file:
            print('Converting to PDF')
            file.write(result)
            os.remove('temp.html')
            print('PDF file is located at : ' + os.path.abspath(output_file))


if __name__ == "__main__":
    html_to_pdf_obj = HtmlToPdfConverter(
        template_vars='book.json',
        html_template='book.html'
    )
    html_to_pdf_obj.create(
        output_file='asdfasdf'
    )
