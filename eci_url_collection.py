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

# List to store URLs
won_links = []
constituency_links = []


# Path to the desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
file_path = os.path.join(desktop_path, "ECI 2024 Party Wise Results.txt")


# Loop through each row in the table
for row in table.find_all('tr')[1:]:  # Skipping the header row
    cells = row.find_all('td')
    if len(cells) > 0:
        won_link = cells[1].find('a')['href'] if cells[1].find('a') else None
        if won_link:
            full_link = base_url + won_link
            won_links.append(full_link)

print(f"Collected {len(won_links)} links.")

# Open the file to write
with open(file_path, 'w') as file:

    # Scraping url for each party to get list of constituency links
    for link in won_links:
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find the table containing the lsit of winning candidates
        table = soup.find('table', {'class': 'table table-striped table-bordered'}) 
        for row in table.find_all('tr')[1:]:  # Skipping the header row
            cells = row.find_all('td')
            if len(cells) > 0:
                constituency_link = cells[1].find('a')['href'] if cells[1].find('a') else None
                if constituency_link:
                    full_link2 = base_url + constituency_link
                    new_full_link2 = full_link2.replace("candidateswise-", "Constituencywise")
            constituency_links.append(new_full_link2)
            file.write(f"{new_full_link2}\n")

print(f"Collected {len(constituency_links)} links.")

