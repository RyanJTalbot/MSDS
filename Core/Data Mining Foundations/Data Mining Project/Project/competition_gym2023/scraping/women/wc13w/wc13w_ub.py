import requests
import pandas as pd
from bs4 import BeautifulSoup

# Define the URL of the Wikipedia page
url = "https://en.wikipedia.org/wiki/2013_World_Artistic_Gymnastics_Championships"

# Send an HTTP GET request to the URL
response = requests.get(url)

# Parse the HTML content of the page using Beautiful Soup
soup = BeautifulSoup(response.text, 'html.parser')

# Find the table you want (in this case, we'll scrape the table at index 21)
tables = soup.find_all('table')

# Check if there are at least 22 tables on the page (since we want table 21)
if len(tables) >= 15:
    table_21 = tables[14]

    # Extract the data from the table and store it in a list of lists
    data = []
    for row in table_21.find_all('tr'):
        cells = row.find_all(['th', 'td'])
        row_data = [cell.get_text(strip=True) for cell in cells]
        data.append(row_data)

    # Convert the data into a DataFrame
    df = pd.DataFrame(data)

    # Save the DataFrame as a CSV file
    df.to_csv('wc13w_ub.csv', index=False, header=False)

    print("Table 21 data has been scraped and saved as wc13w_ub.csv.")
else:
    print("Table 21 not found on the page.")
