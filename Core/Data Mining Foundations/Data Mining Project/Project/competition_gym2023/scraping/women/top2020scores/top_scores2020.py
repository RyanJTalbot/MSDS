import pandas as pd

# Specify the URL of the page containing the tables
url = 'https://thegymter.net/the-best-scores-in-2020/'

# Use pandas to read the HTML tables on the page
tables = pd.read_html(url)

# Loop through each table and save it as a separate CSV file
for i, table in enumerate(tables):
    # Drop rows with all NaN values
    table.dropna(how='all', inplace=True)

    # Reset the index
    table.reset_index(drop=True, inplace=True)

    # Save the DataFrame to a CSV file
    filename = f'/Users/ryantalbot/Desktop/MSDS/table_{i}.csv'
    table.to_csv(filename, index=False)
    print(f'Saved table {i} to {filename}')
