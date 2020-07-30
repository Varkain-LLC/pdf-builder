import os
import pdfkit


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
assetsFolder = os.path.join(BASE_DIR, '../assets/')

options = { 
    'footer-right': '[page] of [topage]',
    'header-center': '[section]',
    'header-line': None,
}  

pdfkit.from_file('templates/book.html', 'out.pdf', options=options)