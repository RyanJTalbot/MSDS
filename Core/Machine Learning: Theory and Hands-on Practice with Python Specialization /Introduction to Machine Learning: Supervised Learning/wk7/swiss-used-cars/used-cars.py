import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import logging

# Configure logging
logging.basicConfig(filename="scraping_errors.log", level=logging.ERROR)

# Base URL with pagination parameter
base_url = "https://en.comparis.ch/carfinder/marktplatz/occasion?page={}"

# List to store car data
car_data = []

# Define headers to mimic a regular browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
}

# Define a function to parse each page with retries


def parse_page(url, page_num):
    for attempt in range(3):  # Retry up to 3 times
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Find car listings on the page
            listings = soup.find_all("div", class_="css-1w1nz0b ehesakb4")
            for listing in listings:
                try:
                    car = {
                        "Model": listing.find("h2", class_="css-roynbj ehesakb5").text.strip(),
                        "Price": listing.find("p", class_="css-1uknu01").text.strip(),
                        "Year": listing.find_all("p", class_="css-1so6dk4")[1].text.strip(),
                        "Mileage": listing.find_all("p", class_="css-1so6dk4")[2].text.strip(),
                        "Fuel Type": listing.find_all("p", class_="css-1so6dk4")[4].text.strip()
                    }
                    car_data.append(car)
                except (AttributeError, IndexError):
                    logging.error(
                        f"Error parsing listing on page {page_num}, skipping it.")
            return True  # Successfully parsed the page
        else:
            logging.error(
                f"Failed to retrieve page {page_num} (Attempt {attempt + 1})")
            time.sleep(5)  # Wait before retrying
    return False  # Failed after 3 attempts


# Loop over multiple pages
for page_num in range(1, 101):  # Scrape pages 1 through 100
    page_url = base_url.format(page_num)
    print(f"Scraping page {page_num}")

    success = parse_page(page_url, page_num)
    if not success:
        logging.error(
            f"Page {page_num} failed after 3 attempts and will be skipped.")

    # Randomize delay between 3 and 7 seconds
    time.sleep(random.uniform(3, 7))

    # Save progress every 10 pages
    if page_num % 10 == 0:
        df = pd.DataFrame(car_data)
        df.to_csv("comparis_car_listings_progress.csv", index=False)
        print(f"Progress saved up to page {page_num}.")

# Final save
df = pd.DataFrame(car_data)
df.to_csv("comparis_car_listings_final.csv", index=False)
print("Scraping complete. Final data saved to comparis_car_listings_final.csv")
