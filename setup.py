from distutils.core import setup

setup(
    name='PDFbuilder',
    version='0.0.2',
    author='Elya',
    author_email='elya@saasuma.com',
    url='https://github.com/Varkain-LLC/PDF-builder/',
    packages=['converter'],
    description='HTML to PDF with Python-Jinja',
    long_description=open('README.md').read(),
    keywords=['pdf', 'pdf_builder', 'pdf-builder', 'PDFbuilder'],
    install_requires=[
        'selenium',
        'jinja2'
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
