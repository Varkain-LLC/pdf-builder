# PDF-builder
pdf builder for fanbooks &amp; JRNL

**OS:** Its most likely to have Linux OS

**Used Technologies:**
- Python 3.x
- Selenium
- Jinja2
- HTML

## Installation
Clone repository, move to project root dir, install dependencies:
```
git clone https://github.com/Varkain-LLC/PDF-builder.git
cd PDF-builder
pip install -r requirements.txt
```
Install chrome (chromium) browser.
```
sudo apt install chromium-browser
```

## Microservice Structure and Demo
Structure:
```
│───assets
│   │   book.json
│   │   ...
│───converter
│   │   converter.py
│   │   ...
│   └───templates
│       │   book.html
│       │   ...
```
Usage:
```
cd converter
python converter.py <json_source> <html_template_source> <filename_to_save>
```
Example:
```
python converter.py /absolute-path-to/assets/book.json jrnl-template.html /absolute-path-to/test.pdf
```
1. `book.json` or json data is required
2. `html_template_source` will be located in `converter/templates` folder
3. `filename_to_save` is the name of the pdf file you want to get.
4. The keys in json file should match to variables in `converter/templates/<html_template_source>` file

## How works this microservice
1. It takes variables from `book.json` by key and puts into some temp.html
2. converts that `temp.html` to `assets/book.pdf`
3. removes `temp.html`

## License
[MIT](https://choosealicense.com/licenses/mit/)

###### Authors and acknowledgment: Special thanks to `https://github.com/maxvst` for `python-selenium-chrome-html-to-pdf-converter` repository
