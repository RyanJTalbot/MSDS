import requests
import csv
from bs4 import BeautifulSoup

# Specify the URL of the Wikipedia page
url = "https://en.wikipedia.org/wiki/Gymnastics_at_the_2019_Summer_Universiade"


# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all tables on the page
    tables = soup.find_all("table")

    # Check if there are at least 9 tables on the page
    if len(tables) >= 22:
        # Select the 9th table (Python uses 0-based indexing)
        table_9 = tables[21]

        # Initialize a CSV file for writing
        with open("uni19fx.csv", mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)

            # Iterate through rows of the table
            for row in table_9.find_all("tr"):
                # Extract data from each cell in the row
                data = [cell.get_text(strip=True)
                        for cell in row.find_all(["th", "td"])]

                # Write the row of data to the CSV file
                writer.writerow(data)

        print("Table data has been saved to uni19fx .csv.")
    else:
        print("There are not enough tables on the page.")
else:
    print("Failed to retrieve the page. Status code:", response.status_code)
