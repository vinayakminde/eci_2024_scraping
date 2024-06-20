import requests
from bs4 import BeautifulSoup
import json
import os
import pandas as pd

## Path to the text file containing the URLs (adjust as needed)
file_path = os.path.expanduser("~/Desktop/ECI 2024 Party Wise Results.txt")

# Path to the Excel file to save the results (adjust as needed)
excel_path = os.path.expanduser("~/Desktop/ECI 2024 Party Wise Results.xlsx")

# Read URLs from the text file
with open(file_path, 'r') as file:
    urls = file.read().splitlines()

# List to store all scraped data
all_data = []

# Iterate through each URL
for url in urls:
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the page content
    soup = BeautifulSoup(response.content, 'html.parser')

     # Extract and process the page title to get the state name
    page_title = soup.title.string
    state = page_title.replace("2024 Indian general election in ", "").strip()

    # Lists to store the scraped data
    constituencies = []
    turnouts = []

    # Flag to indicate if the table is found
    table_found = False


    # Iterate through all tables on the page
    for table in soup.find_all('table', {'class': 'wikitable'}):
        # Find the header row
        headers = table.find('tr').find_all('th')
        header_texts = [header.text.strip() for header in headers]

        # Check if both 'Constituency' and 'Turnout' are in the headers
        if 'Constituency' in header_texts and 'Turnout' in header_texts and 'Winner' in header_texts:
            constituency_index = header_texts.index('Constituency')
            turnout_index = header_texts.index('Turnout')

            # Iterate through the table rows and extract data
            for row in table.find_all('tr')[1:]:  # Skip the header row
                cells = row.find_all('td')
                if len(cells) > max(constituency_index, turnout_index):  # Ensure the row has enough columns
                    constituency = cells[constituency_index].text.strip()
                    turnout = cells[turnout_index].text.strip()

                    # Convert turnout to a number with decimal
                    try:
                        turnout = float(turnout.replace('%', '').strip())
                    except ValueError:
                        turnout = None  # Handle cases where turnout is not a valid number

                    constituencies.append(constituency)
                    turnouts.append(turnout)

     # Combine data and add to the all_data list
    for constituency, turnout in zip(constituencies, turnouts):
        all_data.append({'State': state, 'Constituency': constituency, 'Turnout': turnout})

# Create a DataFrame from the collected data
df = pd.DataFrame(all_data)

# Save the DataFrame to an Excel file
df.to_excel(excel_path, index=False)

print(f"Data successfully scraped and saved to {excel_path}")
