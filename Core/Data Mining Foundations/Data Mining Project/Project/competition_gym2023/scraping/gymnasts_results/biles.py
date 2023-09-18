import requests
from bs4 import BeautifulSoup
import csv

# URL of the page containing the table
url = "https://thegymter.net/simone-biles/"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all tables on the page
    tables = soup.find_all("table")

    # Check if there are at least two tables on the page
    if len(tables) >= 2:
        # Select the second table (index 1)
        table = tables[1]

        # Initialize a list to store table data
        data = []

        # Iterate through table rows
        for row in table.find_all("tr"):
            # Extract table data (td) from each row
            columns = row.find_all("td")
            row_data = [column.get_text(strip=True) for column in columns]

            # Append the row data to the list
            data.append(row_data)

        # Specify the CSV file name
        csv_file = "biles23.csv"

        # Write the table data to the CSV file
        with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            for row in data:
                writer.writerow(row)

        print(f"Data has been exported to {csv_file}.")
    else:
        print("There are not enough tables on the page.")
else:
    print("Failed to retrieve the page. Status code:", response.status_code)
