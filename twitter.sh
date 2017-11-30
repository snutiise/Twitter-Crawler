#!/bin/bash

cd /home/my/crawler/twitter
PATH=$PATH:/usr/local/bin
export PATH
scrapy crawl twitter
python thumb.py
