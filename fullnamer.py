#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import urlparse
import cPickle


def fix_url(url):
    parsed_url = urlparse.urlparse(url)
    if parsed_url.netloc == '' and parsed_url.scheme == '':
        fixed_url = urlparse.urljoin(u'https://мвд.рф', parsed_url.path)
        return fixed_url
    elif parsed_url.netloc != '' and parsed_url.scheme in ['http', 'https']:
        return url
    else:
        print 'Error in URL: {}'.format(url)


def get_urls(url):
    urls = []
    html = requests.get(url, headers=useragent)
    soup_data = BeautifulSoup(html.text, 'html.parser')
    main_divs = soup_data.find_all('ul', class_='structure-link-list')
    for main_div in main_divs:
        divisions = main_div.find_all('a')
        for division in divisions:
             url = fix_url(division['href'])
             urls.append(url)
    return urls


def get_people(url):
    html = requests.get(url, headers=useragent)
    soup_data = BeautifulSoup(html.text, 'html.parser')
    ministers_block = soup_data.find_all('a', class_='e-popup_minister')
    for minister in ministers_block:
        raw_name = minister.find('span', class_='minister_full_name')
        raw_title = minister.find('span', class_='minister_title')
        name = raw_name.text.strip()
        title = raw_title.text.strip()
        minister = name, title
        print minister[0]
        yield minister


def unpick(_from, file_name):
    with open(file_name, 'wb') as fout:
        cPickle.dump(_from, fout)


useragent = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36'}

begin_url = u'https://мвд.рф/mvd/structure1'
people = []
all_urls = get_urls(begin_url)

for p in get_people(begin_url):
    people.append(p)

for url in all_urls[:2]:
    for p in get_people(url):
        people.append(p)

