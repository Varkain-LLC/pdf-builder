from distutils.core import setup

setup(
    name='pdfbuilder',
    version='0.0.3',
    author='Elya',
    author_email='elya@saasuma.com',
    url='https://github.com/Varkain-LLC/PDF-builder/',
    packages=['html2pdf_converter'],
    description='HTML to PDF with Python-Jinja',
    long_description=open('README.md').read(),
    keywords=['pdf', 'pdf_builder', 'pdf-builder', 'PDFbuilder', 'pdfbuilder'],
    install_requires=[
        'selenium==3.141.0',
        'jinja2==2.11.2'
    ],
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'Development Status :: 1 - Beta'
    ]
)
