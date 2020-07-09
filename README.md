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

## Demo
```
cd converter
python converter.py
```

## About this microservice structure
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
1. In `assets` folder you can find `book.json` file
2. The keys are match to variables in `converter/templates/book.html` file

## How works this microservice
1. It takes variables from `book.json` by key and puts into some temp.html
2. converts that `temp.html` to `assets/book.pdf`
3. removes `temp.html` 

## License
[MIT](https://choosealicense.com/licenses/mit/)

###### Authors and acknowledgment: Special thanks to `https://github.com/maxvst` for `python-selenium-chrome-html-to-pdf-converter` repository
