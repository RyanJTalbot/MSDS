import pandas as pd

# Specify the URL of the page containing the table
url = 'https://thegymter.net/2013/03/25/2013-cottbus-world-cup-results/'

# Use pandas to read the HTML tables on the page
tables = pd.read_html(url)

# Assuming the table you want is the first one on the page, you can access it like this:
df = tables[2]

# Drop rows with all NaN values
df.dropna(how='all', inplace=True)

# Reset the index
df.reset_index(drop=True, inplace=True)

# Display the DataFrame
print(df)
# Save the DataFrame to a CSV file
df.to_csv('/Users/ryantalbot/Desktop/MSDS/worldcup2013cott_bb.csv', index=False)
