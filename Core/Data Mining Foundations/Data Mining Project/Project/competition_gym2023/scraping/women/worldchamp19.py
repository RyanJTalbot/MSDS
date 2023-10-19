

import requests
from bs4 import BeautifulSoup
import csv

# URL of the webpage containing the table
url = "https://en.wikipedia.org/wiki/2019_World_Artistic_Gymnastics_Championships#Women's_results"

# Send a GET request to the URL
response = requests.get(url)
html = response.text

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Find all the table elements on the page
tables = soup.find_all('table', class_='wikitable')

# Check if there are at least two tables on the page
if len(tables) >= 14:
    # Select the second table
    table = tables[13]

    # Initialize a list to store data
    data = []

    # Iterate through rows of the table body
    for row in table.find('tbody').find_all('tr'):
        cols = row.find_all(['th', 'td'])
        cols = [col.get_text(strip=True) for col in cols]
        data.append(cols)

    # Specify the CSV file name
    csv_filename = 'Women2019_World_Artistic_Gymnastics_Championships.csv'

    # Write the data to the CSV file
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(data)

    print(f"Data saved to {csv_filename}")
else:
    print("Not enough tables found on the page.")
