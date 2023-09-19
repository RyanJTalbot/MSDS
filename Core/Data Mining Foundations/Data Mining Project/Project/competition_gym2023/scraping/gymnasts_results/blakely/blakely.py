import requests
from bs4 import BeautifulSoup
import csv

# URL of the page containing the tables
url = "https://thegymter.net/skye-blakely/"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all tables on the page
    tables = soup.find_all("table")

    # Check if there are at least four tables on the page
    if len(tables) >= 4:
        # Select the second table (index 1), third table (index 2), and fourth table (index 3)
        table2 = tables[1]
        table3 = tables[2]
        table4 = tables[3]

        # Initialize a list to store table data for the second table
        data2 = []

        # Iterate through table rows for the second table
        for row in table2.find_all("tr"):
            # Extract table data (td) from each row
            columns = row.find_all("td")
            row_data = [column.get_text(strip=True) for column in columns]

            # Append the row data to the list for the second table
            data2.append(row_data)

        # Initialize a list to store table data for the third table
        data3 = []

        # Iterate through table rows for the third table
        for row in table3.find_all("tr"):
            # Extract table data (td) from each row
            columns = row.find_all("td")
            row_data = [column.get_text(strip=True) for column in columns]

            # Append the row data to the list for the third table
            data3.append(row_data)

        # Initialize a list to store table data for the fourth table
        data4 = []

        # Iterate through table rows for the fourth table
        for row in table4.find_all("tr"):
            # Extract table data (td) from each row
            columns = row.find_all("td")
            row_data = [column.get_text(strip=True) for column in columns]

            # Append the row data to the list for the fourth table
            data4.append(row_data)

        # Specify the CSV file names
        csv_file2 = "blakely23.csv"
        csv_file3 = "blakely22.csv"
        csv_file4 = "blakely21.csv"

        # Write the table data to the CSV files for the second, third, and fourth tables
        with open(csv_file2, mode="w", newline="", encoding="utf-8") as file2:
            writer2 = csv.writer(file2)
            for row in data2:
                writer2.writerow(row)

        with open(csv_file3, mode="w", newline="", encoding="utf-8") as file3:
            writer3 = csv.writer(file3)
            for row in data3:
                writer3.writerow(row)

        with open(csv_file4, mode="w", newline="", encoding="utf-8") as file4:
            writer4 = csv.writer(file4)
            for row in data4:
                writer4.writerow(row)

        print(f"Data from the second table has been exported to {csv_file2}.")
        print(f"Data from the third table has been exported to {csv_file3}.")
        print(f"Data from the fourth table has been exported to {csv_file4}.")
    else:
        print("There are not enough tables on the page.")
else:
    print("Failed to retrieve the page. Status code:", response.status_code)
