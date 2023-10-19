import requests
from bs4 import BeautifulSoup

url = "https://www.olympiandatabase.com/index.php?id=45632&L=1"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

main_container = soup.find('div', class_='main_container')
frame_space_table = main_container.find('table', class_='frame_space')

if frame_space_table is not None:
    print("Found frame_space_table")
    table_body = frame_space_table.find('tbody')

    if table_body is not None:
        print("Found table_body")

        rows = table_body.find_all('tr')

        for row in rows:
            td_elements = row.find_all('td')
            for td in td_elements:
                print(td.get_text())
    else:
        print("No table_body found")
else:
    print("No frame_space_table found")
