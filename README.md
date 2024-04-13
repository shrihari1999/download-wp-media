# Wordpress media downloader
The fastest way to download all media from any wordpress site.

## Install
As a prerequisite, make sure you have python, pip and pipenv installed.

Activate shell, install required packages and run
```
pipenv shell
pipenv install
```

## Usage
The script accepts the following positional and optional arguements
```
positional arguments:
  domain               wordpress domain

optional arguments:
  -h, --help           show this help message and exit
  --max_page MAX_PAGE  max number of pages to scan
  --per_page PER_PAGE  number of media elements per page
```

For help, run
```
python download_wp_media.py -h
```

Example
```
python download_wp_media.py example.com
```



