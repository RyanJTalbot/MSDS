import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL (adjust for pagination as needed)
base_url = "https://example.com/houses?page="

# Initialize a list to store the data
houses_data = []

# Define the number of pages you want to scrape
num_pages = 5  # Adjust as needed

for page in range(1, num_pages + 1):
    # Fetch the page
    url = f"{base_url}{page}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all house listings on the page
    listings = soup.find_all('h2', class_="css-fw9263-AggregatesListingCard")

    for listing in listings:
        # Extract each detail
        try:
            agency = listing.find(
                'div', class_="css-1mtsvd6-AggregatesListingCard").text.strip()
            house_type = listing.find(
                'div', class_="css-qb670f-AggregatesListingCard").text.strip()
            description = listing.find(
                'div', class_="css-1lelbas-AggregatesListingCard").text.strip()
            location = listing.find(
                'div', class_="css-1wo7mki-AggregatesListingCard").text.strip()

            # Extract price details
            price_tag = listing.find_next_sibling(
                'div').find('div', class_="css-1r801wc")
            price = price_tag.text.strip() if price_tag else "N/A"

            # Extract price per square meter
            price_per_sqm_tag = listing.find_next_sibling('div').find(
                'div', class_="css-1eo6i6u-AggregatesListingCard")
            price_per_sqm = price_per_sqm_tag.text.strip() if price_per_sqm_tag else "N/A"

            # Add to list as a dictionary
            houses_data.append({
                "Agency": agency,
                "Type": house_type,
                "Description": description,
                "Location": location,
                "Price": price,
                "Price per m²": price_per_sqm
            })
        except AttributeError:
            # Handle any missing data
            continue

# Convert to DataFrame and display
df = pd.DataFrame(houses_data)
print(df)
