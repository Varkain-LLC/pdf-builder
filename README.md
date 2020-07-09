# PDF-builder
pdf builder for fanbooks &amp; JRNL

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
python converter.py <json_source> <html_template_sourse> <filename_to_save>
```
Example:
```
python converter.py book.json book.html book.pdf
```
1. `book.json` should be located in `assets` folder 
2. `book.html` will be located in `converter/templates` folder
3. `book.pdf` is the name of the pdf file you want to get.
4. The keys in json file should match to variables in `converter/templates/book.html` file

## How works this microservice
1. It takes variables from `book.json` by key and puts into some temp.html
2. converts that `temp.html` to `assets/book.pdf`
3. removes `temp.html` 

## License
[MIT](https://choosealicense.com/licenses/mit/)

###### Authors and acknowledgment: Special thanks to `https://github.com/maxvst` for `python-selenium-chrome-html-to-pdf-converter` repository
