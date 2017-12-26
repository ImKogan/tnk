'''
names_to_json.py

TODO(IK) add comments to file
'''
import os
import re
import json
from time import time

def partition_sorted_lists(list_a, list_b):
    '''
    partition two sorted lists into disjunction (a\b and b\a) and intersection
    '''
    list_a_not_in_b = []
    list_b_not_in_a = []
    list_intersection = []

    i, j = 0, 0
    while i < len(list_a) and j < len(list_b):
        if list_a[i] < list_b[j]:
            list_a_not_in_b.append(list_a[i])
            i += 1
        elif list_b[j] < list_a[i]:
            list_b_not_in_a.append(list_b[j])
            j += 1
        else:
            list_intersection.append(list_b[j])
            i += 1
            j += 1

    return list_a_not_in_b, list_b_not_in_a, list_intersection

def occurances_of_biblical_words_not_in_list(word_list, bible_books_dict={}):
    '''
    filter out all words in word_list occuring in bible_books_dict and return the rest in a dict
    '''
    ### remove punctualization with exception dash (which is sometimes used in names)
    punctuation_pattern = re.compile(r'[!"#$%&()*+\',./:;<=>?@\[\]^_`{}~]|[-]{2}')

    not_in_word_list = {}
    in_word_list = {}
    for book in bible_books_dict.values():
        for chapter in book:
            for verse in chapter:
                verse = punctuation_pattern.sub(' ', verse)
                for word in verse.split(' '):
                    if word in not_in_word_list:
                        not_in_word_list[word] += 1
                    elif word in in_word_list:
                        pass
                    elif word in word_list:
                        in_word_list[word] = 1
                    else:
                        not_in_word_list[word] = 1

    return not_in_word_list


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
            if line[0].isupper():
                capital_words.append(line.strip())
            else:
                words.append(line.strip())

    print("words", len(words))
    print("capital_words", len(capital_words))
    words_capitalized = [word.capitalize() for word in words]
    ### we now create separate words only in 'capital_words'
    ### words only in 'words_capitalized' and words appearing in both lists

    words_capitalized_regular, capital_words_not_repeated, cap_repeated_in_lower = \
        partition_sorted_lists(words_capitalized, capital_words)

    print("words_capitalized_regular", len(words_capitalized_regular))
    print("capital_words_not_repeated", len(capital_words_not_repeated))
    print("cap_repeated_in_lower", len(cap_repeated_in_lower))

    ### regular_words is list containing uncapitalized words (words),
    ### capitalized words not appearing in 'capital_words' (words_capitalized_regular),
    ### and words appearing in both capital and non capital form (cap_repeated_in_lower)
    regular_words = words + words_capitalized_regular + cap_repeated_in_lower
    with open(os.path.join(options["local_json"], options["bible"]), 'r') as bible:
        bible_books_dict = json.load(bible)

    print(bible_books_dict.keys())

    ### separate all words in bible_books_dict (text of bible) into two dictionaries;
    ### not_english - storing a count of words not found in 'regular_words' list,
    ### and english - used as a cache of regular_words already encountered

    ### This is a nested function 4 deep - should take about 15 seconds
    start = time()
    not_english = occurances_of_biblical_words_not_in_list(regular_words, bible_books_dict)
    print('################################')
    print(time()-start)
    print('################################')

    other_endings = [word for word in not_english if word.endswith('eth') or \
    word.endswith('est') or word.endswith('ers') or word.endswith('ings')]

    for val in other_endings:
        del not_english[val]

    to_review = [word for word in not_english if word.islower() or word.isupper()]

    for val in to_review:
        del not_english[val]

    not_proper_names = [word for word in not_english if word.endswith('ite') \
    or word.endswith('ites') or word.endswith('ian') or word.endswith('ians')]

    hyphenated_words = []
    for word in not_english:
        if '-' in word:
            split_word = word.split('-')
            if all(element in regular_words for element in split_word):
                hyphenated_words.append(word)

    hyphenated_words.remove('Lo-debar')
    not_proper_names = not_proper_names + hyphenated_words

    for val in not_proper_names:
        if len(val) > 5:
            del not_english[val]

    ss_end = [name for name in not_english if name.endswith('ss')]

    for val in ss_end:
        del not_english[val]

    del not_english[""]
    del not_english["Canst"]
    print(not_english, len(not_english))

    with open(os.path.join(options["local_json"], options["bible_names"]), 'w') as bible_names:
        json.dump(not_english, bible_names, ensure_ascii=False)

if __name__ == '__main__':
    main()
