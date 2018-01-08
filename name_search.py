'''
names_search.py

Allows user to type a text string in the shell as input and returns a
list index of occurances of that string in the bible, if the string is a proper name.
Otherwise, user is notified string is not a proper name in the bible.
'''
import os
import json

def main():
    '''
    Allow user input to search names_index
    '''
    with open("config.json") as config:
        options = json.load(config)
    if os.path.exists(options["local_json"]):
        with open(os.path.join(options["local_json"],
                               options["bible_names_index"]), 'r') as names_index:
            bible_names_index = json.load(names_index)
    else:
        print("'local_json folder does not exists. Please run\n \
             'get_jps.py', 'parse_html.py' and 'names_to_json.py' before running this script.")
        return

    print("Now you can enter a name to search for its occurances in the bible.\n \
        If the text string is a proper name in the bible,\n \
        the output will return an index as a list.")
    search = True
    while search:
        name = input("Please enter the name to search: ")

        if bible_names_index.get(name) is not None:
            print(bible_names_index[name])
        else:
            print("There is no such name in the bible.")
        key = input("If you are done searching, type 'x' , otherwise press 'Enter' key:")
        if key == 'x':
            search = False

if __name__ == '__main__':
    main()
