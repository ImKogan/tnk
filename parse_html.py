'''
parse_html.py

TODO(IK) add comments to file
'''
import os
import glob
import re
from collections import defaultdict
import json
from time import time

from bs4 import BeautifulSoup

def file_to_soup(files):
    '''
    pass list of file names to a corresponding list of BeautifulSoup objects
    '''
    soup_list = []
    for file in files:
        with open(file, encoding='utf-8', errors='ignore') as chapter_file:
            soup_list.append(BeautifulSoup(chapter_file, 'lxml'))
    return soup_list

def clean_soup(soup):
    '''
    parse BeautifulSoup object - a chapter from html file
    and pass text content into list of - book_name, chapter, verse_list
    '''
    text_name = soup.find('h1').text
    assert 'Chapter ' in text_name
    text_name = text_name.replace('Chapter ', '')
    text_name = text_name.rsplit(' ', 1)
    book_name = text_name[0]
    chapter = text_name[1]
    # verses are <p> that start with a digit
    verses = [p.text for p in soup.find_all('p') if p.text[0].isdigit()]
    text = '\n'.join(verses)
    # remove strings of the form {P} and {S} and verse numbers
    # TODO(IK) investigate and fix backslashes in regex
    ps_pattern = re.compile('\s*\{[A-Za-z]\}') #pylint3: disable=anomalous-backslash-in-string
    num_pattern = re.compile('[0-9]+\s*')
    text = ps_pattern.sub("", text)
    text = num_pattern.sub("", text)
    verse_list = re.split('\s*\n\s*', text)

    return [book_name, chapter, verse_list]

def chapter_list_to_dict(chapter_list):
    '''
    create a dict with book names as keys and a list of lists as values
    where each sublist is a chpater. chapters are ordered by their order in the book
    '''
    chapter_list.sort(key=lambda x: (x[0], int(x[1])))
    bible_books_dict = defaultdict(list)
    for item in chapter_list:
        book = item[0]
        chapter = item[1]
        text = item[2]
        bible_books_dict[book].append(text)
        assert len(bible_books_dict[book]) == int(chapter)
    return bible_books_dict

def main():
    '''
    parse list of htm_files and output bible as json
    '''
    with open("config.json") as config:
        options = json.load(config)

    # ask about this configuration

    if os.path.exists(options["local_json"]):
        pass
    else:
        os.mkdir(options["local_json"])

    htm_files = glob.glob(os.path.join(options["local_jps_html"], "et/et????*.htm"))
    soup_list = file_to_soup(htm_files)
    chapter_list = []
    start = time()
    for soup in soup_list:
        chapter_list.append(clean_soup(soup))
    print(time()-start)
    bible_books_dict = chapter_list_to_dict(chapter_list)

    with open(os.path.join(options["local_json"], options["bible"]), 'w') as bible_json:
        json.dump(bible_books_dict, bible_json, ensure_ascii=False)

if __name__ == '__main__':
    main()
