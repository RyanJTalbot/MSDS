import requests
from bs4 import BeautifulSoup

# URL of the webpage to scrape
url = "https://www.gymnastics.sport/site/rankings/ranking_wag.php"

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table with the specified ID
    table = soup.find('table', {'class': 'table table-striped'})

    # Check if the table was found
    if table:
        # Loop through table rows (skipping the header rows)
        for row in table.select('tbody tr'):
            # Extract data from table cells
            cells = row.find_all('td')
            if cells:
                # Print data from each cell
                for cell in cells:
                    print(cell.text.strip())
                print("------------------------")
    else:
        print("Table not found on the webpage.")
else:
    print("Failed to retrieve the webpage.")
