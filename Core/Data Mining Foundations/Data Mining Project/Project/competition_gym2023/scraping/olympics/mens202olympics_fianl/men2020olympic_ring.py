
import requests
from bs4 import BeautifulSoup
import csv

# URL of the webpage containing the table
url = "https://en.wikipedia.org/wiki/Gymnastics_at_the_2020_Summer_Olympics_%E2%80%93_Men%27s_rings"

# Send a GET request to the URL
response = requests.get(url)
html = response.text

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Find all the table elements on the page
tables = soup.find_all('table', class_='wikitable')

# Check if there are at least two tables on the page
if len(tables) >= 3:
    # Select the second table
    table = tables[2]

    # Initialize a list to store data
    data = []

    # Iterate through rows of the table body
    for row in table.find('tbody').find_all('tr'):
        cols = row.find_all(['th', 'td'])
        cols = [col.get_text(strip=True) for col in cols]
        data.append(cols)

    # Specify the CSV file name
    csv_filename = 'Gymnastics_ 2020_Olympics_Men\'s_artistic_rings.csv'

    # Write the data to the CSV file
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(data)

    print(f"Data saved to {csv_filename}")
else:
    print("Not enough tables found on the page.")
