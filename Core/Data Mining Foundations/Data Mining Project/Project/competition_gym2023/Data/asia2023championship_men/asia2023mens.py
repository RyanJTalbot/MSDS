import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the Wikipedia page
url = "https://en.wikipedia.org/wiki/2023_Asian_Artistic_Gymnastics_Championships"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all tables on the page
    tables = soup.find_all("table")

    # Define table indices for the tables you want to scrape
    table_indices = [7, 8, 9, 10, 11, 12, 13]  # Indices of the desired tables

    for table_index in table_indices:
        # Check if the specified table index is valid
        if 0 <= table_index < len(tables):
            # Select the specified table
            selected_table = tables[table_index]

            # Use pandas to read the table into a DataFrame
            df = pd.read_html(str(selected_table))[0]

            # Define a mapping of table index to file name
            file_name_mapping = {
                7: "mens2023iaa.csv",
                8: "floor23mens.csv",
                9: "ph23mens.csv",
                10: "rings23mens.csv",
                11: "vault23mens.csv",
                12: "pb23mens.csv",
                13: "hb23mens.csv"
            }

            # Get the file name based on the table index
            file_name = file_name_mapping.get(table_index, "table.csv")

            # Save the DataFrame to a CSV file
            df.to_csv(file_name, index=False)

            print(
                f"Table {table_index} data has been exported to '{file_name}'.")
        else:
            print(f"Invalid table index: {table_index}")
else:
    print("Failed to retrieve the page. Status code:", response.status_code)
