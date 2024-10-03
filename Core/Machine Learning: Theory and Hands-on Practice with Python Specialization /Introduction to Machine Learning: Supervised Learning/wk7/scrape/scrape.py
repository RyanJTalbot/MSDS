import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Specify the path to your chromedriver
chrome_driver_path = "/usr/local/bin/chromedriver"


# Create a Service object
service = Service(executable_path=chrome_driver_path)

# Initialize the WebDriver using the Service object
driver = webdriver.Chrome(service=service)

# Navigate to the target URL
driver.get("https://www.homegate.ch/buy/real-estate/sc-single-house/country-switzerland/matching-list?o=dateCreated-desc&loc=geo-canton-geneve")

# Let the page load fully
driver.implicitly_wait(10)

# Extract data using Selenium
listings = driver.find_elements(
    By.CLASS_NAME, 'HgCardElevated_cardElevated_M4Ozt')

data = []
for listing in listings:
    try:
        # Get the price
        price = listing.find_element(
            By.CLASS_NAME, 'HgListingCard_price_JoPAs').text

        # Get rooms and living space
        details = listing.find_element(
            By.CLASS_NAME, 'HgListingRoomsLivingSpace_roomsLivingSpace_GyVgq')
        rooms = details.find_elements(By.TAG_NAME, 'strong')[0].text
        living_space = details.find_elements(By.TAG_NAME, 'strong')[1].text

        # Get address
        address = listing.find_element(By.TAG_NAME, 'address').text

        # Append to data list
        data.append({
            'Price': price,
            'Rooms': rooms,
            'LivingSpace': living_space,
            'Address': address
        })
    except Exception as e:
        print(f"Error extracting data: {e}")

# Convert to DataFrame (assuming you have Pandas installed)
df = pd.DataFrame(data)
print(df.head())

# Close the driver
driver.quit()
