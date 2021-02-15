from setuptools import setup

setup(
    name='pdfbuilder',
    version='0.1.0',
    author='Smirnov.EV',
    author_email='knyazz@gmail.com',
    url='https://github.com/Varkain-LLC/PDF-builder/',
    packages=['html2pdf_converter', 'html2pdf_converter.tools'],
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
