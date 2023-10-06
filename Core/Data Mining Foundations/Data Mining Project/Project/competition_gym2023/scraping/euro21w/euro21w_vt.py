import requests
import pandas as pd
from bs4 import BeautifulSoup

# Define the URL of the Wikipedia page
url = "https://en.wikipedia.org/wiki/2021_European_Artistic_Gymnastics_Championships#Individual_all-around_2"

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all the tables on the page
    tables = soup.find_all("table")

    # Check if there are at least 32 tables on the page
    if len(tables) >= 23:
        # Extract the 32nd table
        target_table = tables[22]  # Python uses 0-based indexing

        # Parse the table data and convert it to a DataFrame
        table_data = []
        for row in target_table.find_all("tr"):
            columns = row.find_all(["td", "th"])
            row_data = [column.get_text(strip=True) for column in columns]
            table_data.append(row_data)

        # Create a DataFrame from the table data
        df = pd.DataFrame(table_data)

        # Save the DataFrame to a CSV file
        df.to_csv("euro21w_vt.csv", index=False, header=False)

        print("Data saved to euro21w_vt.csv")

    else:
        print("There are not enough tables on the page.")
else:
    print("Failed to retrieve the web page. Status code:", response.status_code)
