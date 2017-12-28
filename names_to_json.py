'''
names_to_json.py

TODO(IK) add comments to file
'''
import os
import re
import json
from collections import defaultdict
from time import time


def irregular_words_not_in_list(word_list, bible_books_dict={}):
    '''
    filter out all words in word_list occuring in bible_books_dict and return the rest in a dict
    '''
    ### remove punctualization with exception dash (which is sometimes used in names)
    not_word_pattern = re.compile(r'[^A-Za-z\-]+|[-]{2}')

    word_list_set = set(word_list)
    not_in_word_list = defaultdict(list)

    for book in bible_books_dict:
        for chapter in bible_books_dict[book]:
            for verse in chapter:
                verse_split = not_word_pattern.sub(' ', verse)
                for word in verse_split.split(' '):
                    if word in word_list_set:
                        pass
                    else:
                        not_in_word_list[word].append([book,
                                                       bible_books_dict[book].index(chapter),
                                                       chapter.index(verse)])

    return not_in_word_list

def is_weird_word(dictionary, word_list):
    other_endings = [word for word in dictionary if word.endswith('eth') or \
    word.endswith('est') or word.endswith('ers') or word.endswith('ings')]

    for val in other_endings:
        del dictionary[val]

    to_review = [word for word in dictionary if word.islower() or word.isupper()]

    for val in to_review:
        del dictionary[val]

    not_proper_names = [word for word in dictionary if word.endswith('ite') \
    or word.endswith('ites') or word.endswith('ian') or word.endswith('ians')]

    hyphenated_words = []
    for word in dictionary:
        if '-' in word:
            split_word = word.split('-')
            if all(element in word_list for element in split_word):
                hyphenated_words.append(word)

    hyphenated_words.remove('Lo-debar')
    not_proper_names = not_proper_names + hyphenated_words

    for val in not_proper_names:
        if len(val) > 5:
            del dictionary[val]

    ss_end = [name for name in dictionary if name.endswith('ss')]

    for val in ss_end:
        del dictionary[val]

    del dictionary[""]
    del dictionary["Canst"]

    return dictionary

def main():
    '''
    Run partition_sorted_lists() to retreive all regular non proper names
    and then run occurances_of_biblical_words_not_in_list() to filter them out
    run additional filters and return dict with propr names as keys and
    number of occurances in bible.json as values. Save to json file
    '''
    with open("config.json") as config:
        options = json.load(config)
    ### read in unix dictionary of English words - separating capitalized words
    capital_words = []
    words = []
    with open(options["word_list"]) as word_list:
        for line in word_list:
            # can use line.strip()
            if line[0].isupper():
                capital_words.append(line.strip())
            else:
                words.append(line.strip())

    words_capitalized = [word.capitalize() for word in words]

    ### regular_words is list containing uncapitalized words (words),
    ### and capitalized_words (words_capitalized)
    regular_words = words + words_capitalized
    with open(os.path.join(options["local_json"], options["bible"]), 'r') as bible:
        bible_books_dict = json.load(bible)

    print(bible_books_dict.keys())

    ### not_english is a dict with the words not in regular_words as keys
    ### and a list of indices (where in the bible these words occur) as values
    start = time()
    not_english = irregular_words_not_in_list(regular_words, bible_books_dict)
    print('################################')
    print(time()-start)
    print('################################')

    not_english = is_weird_word(not_english, regular_words)
    print(not_english, len(not_english))

    with open(os.path.join(options["local_json"], options["bible_names"]), 'w') as bible_names:
        json.dump(not_english, bible_names, ensure_ascii=False)

if __name__ == '__main__':
    main()
