import requests
from bs4 import BeautifulSoup
import os
import pandas as pd

# URL of the page to be scraped
url = "https://results.eci.gov.in/PcResultGenJune2024/index.htm"
base_url = "https://results.eci.gov.in/PcResultGenJune2024/"

# Make a request to the website
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')

# Find the table containing the election results
table = soup.find('table', {'class': 'table'}) 

# Path to the desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
file_path = os.path.join(desktop_path, "ECI 2024 Party Wise Results.txt")

# Open the file to write
with open(file_path, 'w') as file:
    # Loop through each row in the table
    for row in table.find_all('tr')[1:]:  # Skipping the header row
        cells = row.find_all('td')
        if len(cells) > 0:
            party_name = cells[0].text.strip()
            won_link = cells[1].find('a')['href'] if cells[1].find('a') else None
            if won_link:
                full_link = base_url + won_link
                file.write(f"Won Link: {full_link}\n")
print(f"Links saved to {file_path}")