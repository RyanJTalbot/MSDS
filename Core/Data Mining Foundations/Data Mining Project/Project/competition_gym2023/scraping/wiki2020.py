# import requests
# from bs4 import BeautifulSoup

# url = "https://en.wikipedia.org/wiki/Gymnastics_at_the_2020_Summer_Olympics_%E2%80%93_Women%27s_artistic_qualification"
# response = requests.get(url)
# soup = BeautifulSoup(response.content, 'html.parser')

# # Find the appropriate divs to reach the target table
# content_div = soup.find('div', id='content')

# if content_div:
#     body_content_div = content_div.find('div', id='bodyContent')
#     if body_content_div:
#         parser_output_div = body_content_div.find('div', class_='mw-parser-output')

#         if parser_output_div:
#             # Find the table within the mw-parser-output div
#             frame_space_table = parser_output_div.find('table', class_='wikitable sortable jquery-tablesorter')

#             if frame_space_table:
#                 print("Found frame_space_table")

#                 table_body = frame_space_table.find('tbody')

#                 if table_body:
#                     print("Found table_body")

#                     rows = table_body.find_all('tr')

#                     for row in rows:
#                         td_elements = row.find_all('td')
#                         for td in td_elements:
#                             print(td.get_text())
#                 else:
#                     print("No table_body found")
#             else:
#                 print("No frame_space_table found")
#         else:
#             print("No mw-parser-output div found")
#     else:
#         print("No bodyContent div found")
# else:
#     print("No content div found")


import requests
import urllib.request
import time

from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from urllib.request import urlopen

url = 'https://en.wikipedia.org/wiki/Epidemiology_of_depression'
html = urlopen(url)

soup = BeautifulSoup(html, 'html.parser')
