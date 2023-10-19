import requests
from bs4 import BeautifulSoup
import csv

# Function to scrape and save table data


def scrape_and_save_table(url, table_index, csv_filename):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all tables on the page
        tables = soup.find_all("table")

        # Check if the specified table index is valid
        if 2 <= table_index <= len(tables):
            # Select the specified table
            selected_table = tables[table_index - 1]

            # Initialize a list to store table data
            data = []

            # Iterate through table rows
            for row in selected_table.find_all("tr"):
                # Extract table data (td) from each row
                columns = row.find_all(["td", "th"])
                row_data = [column.get_text(strip=True) for column in columns]

                # Append the row data to the list
                data.append(row_data)

            # Write the table data to the CSV file
            with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                for row in data:
                    writer.writerow(row)

            print(
                f"Table {table_index} data has been exported to {csv_filename}.")
        else:
            print("Invalid table index.")
    else:
        print("Failed to retrieve the page. Status code:", response.status_code)


# URL of the page
url = "https://thegymter.net/katelyn-jong/"

# Scrape and save the second table as "jones23.csv"
scrape_and_save_table(url, 2, "jong23.csv")

# Scrape and save the third table as "jones22.csv"
scrape_and_save_table(url, 3, "jong22.csv")

# Scrape and save the fourth table as "jones21.csv"
scrape_and_save_table(url, 4, "jong21.csv")
