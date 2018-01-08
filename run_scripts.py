'''
run_scripts.py

Run all scripts of the project. Downloads JPS bible, outputs to JSON.
Creates JSON of proper names and their indices, and allows user to search
by inputing a string - outputs index if string is proper name.
'''

import get_jps
import parse_html
import names_to_json
import name_search

get_jps.main()
parse_html.main()
names_to_json.main()
name_search.main()
