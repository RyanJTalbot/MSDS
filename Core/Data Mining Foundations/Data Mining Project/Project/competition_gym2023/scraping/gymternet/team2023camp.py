import requests
from bs4 import BeautifulSoup
import csv

# URL of the webpage containing the table
url = "https://thegymter.net/2023/07/14/2023-july-u-s-national-team-camp-results/"

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table based on its class attribute
    table = soup.find('table')

    # Check if the table is found
    if table:
        # Initialize lists to store table data
        headers = []
        data = []

        # Extract table headers (column names)
        header_row = table.find('tr')
        for header in header_row.find_all('strong'):
            headers.append(header.text.strip())

        # Extract table data rows
        rows = table.find_all('tr')[1:]  # Skip the first row (header row)
        for row in rows:
            row_data = [data.text.strip() for data in row.find_all('td')]
            data.append(row_data)

        # Specify the CSV file name
        csv_file = "team2023camp.csv"

        # Write the data to the CSV file
        with open(csv_file, 'w', newline='') as file:
            writer = csv.writer(file)

            # Write the headers
            writer.writerow(headers)

            # Write the data rows
            writer.writerows(data)

        print(f"Table data has been saved to {csv_file}.")
    else:
        print("Table not found on the webpage.")
else:
    print("Failed to fetch the webpage. Status code:", response.status_code)
