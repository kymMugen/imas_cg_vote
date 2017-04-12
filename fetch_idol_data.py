# coding: utf-8

import urllib.request
from bs4 import BeautifulSoup


def fetch():
    url = 'https://imascg-slstage-wiki.gamerch.com/' \
        '%E3%82%A2%E3%82%A4%E3%83%89%E3%83%AB%E4%B8%80%E8%A6%A7'
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, 'lxml')

    data_source = []

    for result in soup.find('tbody').find_all('td'):
        if result.get('data-col') == '0':
            name_and_attribute = {'attribute': result.text}
        if result.get('data-col') == '1':
            name_and_attribute['name'] = result.text
            data_source.append(name_and_attribute)

    return data_source
