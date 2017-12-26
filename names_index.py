'''
names_index.py

TODO(IK) add comments to file
'''
import os
import re
from collections import defaultdict
import json
from time import time

def bible_index_of_dict_words(dict_words, bible_books_dict={}):
    '''
    traverse dict_words and populate new dict with same keys as dict_words
    with index location in bible_books_dict as values
    '''
    words_index = defaultdict(list)
    ### remove punctualization with exception dash (which is sometimes used in names)
    pattern = re.compile(r'[!"#$%&()*+\',./:;<=>?@\[\]^_`{}~]|[-]{2}')
    for name in dict_words:
        j = 0
        while j < dict_words[name]:
            ### the bible_books_dict is sorted to have persistent index_dict result
            for title, book in sorted(bible_books_dict.items()):
                for chapter in book:
                    num = 0
                    for verse in chapter:
                        if name in verse:
                            verse = pattern.sub(' ', verse)
                            for word in verse.split(' '):
                                if name == word:
                                    words_index[name].append([title, book.index(chapter), num])
                                    j += 1
                        num += 1
    return words_index

def main():
    '''
    run bible_index_of_dict_words() on bible_names and check for accuracy.
    save resulting dict to json.
    '''
    with open("config.json") as config:
        options = json.load(config)
    with open(os.path.join(options["local_json"], options["bible"]), 'r') as bible:
        bible_books_dict = json.load(bible)

    with open(os.path.join(options["local_json"], options["bible_names"]), 'r') as bible_names:
        bible_names_dict = json.load(bible_names)

    start = time()
    bible_names_index = bible_index_of_dict_words(bible_names_dict, bible_books_dict)
    print(time()-start)
    assert len(bible_names_index) == len(bible_names_dict)
    wrong = []
    for name in bible_names_index:
        if len(bible_names_index[name]) != bible_names_dict[name]:
            wrong.append(name)

    assert len(wrong) == 0

    with open(os.path.join(options["local_json"], options["bible_names_index"]), 'w') as names_index:
        json.dump(bible_names_index, names_index, ensure_ascii=False)

if __name__ == '__main__':
    main()
