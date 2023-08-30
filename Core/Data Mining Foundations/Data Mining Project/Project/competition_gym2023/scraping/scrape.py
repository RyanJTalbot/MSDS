# import requests
# from bs4 import BeautifulSoup

# # URL of the page to scrape
# url = "https://thegymter.net/2023/08/28/2023-u-s-championships-results/"

# # Send a GET request to the URL
# response = requests.get(url)

# # Parse the HTML content using BeautifulSoup
# soup = BeautifulSoup(response.content, "html.parser")

# import requests
# response = requests.get(
#     "https://thegymter.net/2023/08/28/2023-u-s-championships-results/")
# if response.status_code != 200:
#     print("Error fetching page")
#     exit()
# else:
#     content = response.content
# print(content)


import csv
import os
import requests
from bs4 import BeautifulSoup

# URL of the page to scrape
url = "https://thegymter.net/2023/08/28/2023-u-s-championships-results/"

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Find the div with class "entry-content"
entry_content_div = soup.find("div", class_="entry-content")

# Find all tables inside the div
tables = entry_content_div.find_all("table")

# Iterate through each table
for table in tables:
    # Find the tbody element inside the table
    tbody = table.find("tbody")

    # Iterate through each row (tr) in the tbody
    for row in tbody.find_all("tr"):
        # Find all cells (td) in the row
        cells = row.find_all("td")

        # Extract and print the content of each cell
        for cell in cells:
            # Extract text and remove extra spaces
            print(cell.get_text(strip=True))
        print("----")  # Separator between rows


# Get the current directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# URL of the page to scrape
url = "https://thegymter.net/2023/08/28/2023-u-s-championships-results/"

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Find the div with class "entry-content"
entry_content_div = soup.find("div", class_="entry-content")

# Find all tables inside the div
tables = entry_content_div.find_all("table")

# List to store data
data_list = []

# Iterate through each table
for table in tables:
    # Find the tbody element inside the table
    tbody = table.find("tbody")

    # Iterate through each row (tr) in the tbody
    for row in tbody.find_all("tr"):
        # Find all cells (td) in the row
        cells = row.find_all("td")

        # Extract text from each cell and add to data_list
        row_data = [cell.get_text(strip=True) for cell in cells]
        data_list.append(row_data)

# Define CSV file path in the same directory as the script
csv_file_path = os.path.join(script_dir, "scraped_data.csv")

# Write data to CSV file
with open(csv_file_path, "w", newline="", encoding="utf-8") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerows(data_list)

print("Data saved to", csv_file_path)
