import argparse
from bs4 import BeautifulSoup, NavigableString, Tag
from selenium import webdriver
from pync import Notifier

"""@bref parser input parameters
"""
parser = argparse.ArgumentParser(description='hackmd-notifier: monitoring specific page.')
parser.add_argument('--link', help='hackmd.io web address')
parser.add_argument('--alarm', help='keyword to activate notifier')
args = parser.parse_args()
link = args.link
alarm = args.alarm

"""@bref open webdriver to parse information from hackmd.io
"""
browser = webdriver.Chrome('/usr/local/bin/chromedriver')
browser.get(link)
html = browser.page_source

soup = BeautifulSoup(html, 'html.parser')

"""@bref find keywords to generate notification
"""
for br in soup.findAll('br'):
    next = br.nextSibling
    if not (next and isinstance(next, NavigableString)):
        continue
    next2 = next.nextSibling
    if next2 and isinstance(next2, Tag):
        text = str(next).strip()
        if text:
            if text == alarm:
                Notifier.notify('Something happened on hackmd.io: {}'.format(link),
                    title='hackmd.io'
                )

browser.close()
