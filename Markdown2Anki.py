"""
    Cameron Johnson 8/20/2018
    https://stackoverflow.com/questions/761824/python-how-to-convert-markdown-formatted-text-to-text
"""

import markdown
from os import listdir
from os.path import isfile, join
from bs4 import BeautifulSoup
import csv

notes_path = "/home/cameronjohnson/Documents/Notes/Cheat Sheets"
markdown_files = [f for f in listdir(notes_path) if isfile(join(notes_path, f))]

for markdown_file in markdown_files:
    with open(join(notes_path, markdown_file), 'r', encoding="utf8") as markdown_file_content:
        md = markdown_file_content.readlines()
        html = markdown.markdown("\n".join(md))
        soup = BeautifulSoup(html)
        root = soup.select_one("hr")
        if root is None:
            continue
        arr = []
        cur_tuple = [root.text, ""]
        while root.next_element is not None:
            element = root.next_element
            if element is not None:
                if element.name == "h1":
                    if cur_tuple[1] != "":
                        arr.append(tuple(cur_tuple))
                    cur_tuple = [element.text, ""]
                elif element.name == "h2":
                    cur_tuple = [cur_tuple[0] + "<br>" + element.text, ""]
                else:
                    try:
                        cur_tuple[1] += str(element) if element.text != cur_tuple[0] else ""
                    except:
                        pass
            root = element
        if cur_tuple[1] != "":
            arr.append(tuple(cur_tuple))
        if len(arr) != 0:
            with open(join(notes_path, 'anki', markdown_file + '.csv'), 'w', encoding="utf8") as csvfile:
                w = csv.writer(csvfile, delimiter=',', doublequote=True)
                for row in arr:
                    w.writerow(row)