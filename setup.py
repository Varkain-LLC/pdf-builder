from distutils.core import setup

setup(
    name='PDF-builder',
    version='0.0.1',
    author='Elya',
    author_email='elya@saasuma.com',
    url='https://github.com/Varkain-LLC/PDF-builder/',
    packages=['converter'],
    description='HTML to PDF with Python-Jinja',
    long_description=open('README.md').read(),
    keywords=['PDF-builder'],
    install_requires=[
        'dselenium',
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
