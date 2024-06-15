import requests
from bs4 import BeautifulSoup
import json
import os
import pandas as pd

# Determine the path to the desktop
desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')

# Path to the text file containing URLs on the desktop
urls_file_path = os.path.join(desktop_path, 'ECI 2024 Party Wise Results.txt')

# Read URLs from the text file
with open(urls_file_path, 'r') as file:
    urls = [line.strip() for line in file.readlines()]

# Initialize a list to store all table data
all_table_data = []

# Function to scrape data from a given URL
def scrape_data(url):
    response = requests.get(url)
    if response.status_code == 200: # Check if the request was successful
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find the header text containing constituency and state information
        header_h2 = soup.find('h2')
        if header_h2:
            span_tag = header_h2.find('span')
            strong_tag = header_h2.find('strong')
            if span_tag and strong_tag:
                constituency = span_tag.text.split('(')[0].strip()
                state = strong_tag.text.strip()[1:-1]
            else:
                constituency = "Unknown Constituency"
                state = "Unknown State"
        else:
            constituency = "Unknown Constituency"
            state = "Unknown State"

        # Find the table containing the data
        table = soup.find('table')

        # Initialize a list to store table data
        table_data = []

        # Check if the table exists
        if table:
            # Iterate through the rows of the table
            for row in table.find_all('tr'):
                # Extract the columns
                cols = row.find_all('td')
                # Get the text from each column and print it
                if cols:
                    cols = [col.text.strip() for col in cols]
                    cols.insert(1, state)  # Insert state after S.N.
                    cols.insert(2, constituency)  # Insert constituency after state
                    table_data.append(cols)
        return table_data
    else:
        print(f"Failed to retrieve the page at {url}")
        return []

# Scrape data from each URL and append it to all_table_data
for url in urls:
    data = scrape_data(url)
    all_table_data.extend(data)

# Path to the Excel file on the desktop
desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
file_path = os.path.join(desktop_path, 'ECI 2024 LS Data.xlsx')

# Specify the order of columns
columns = ["S.N.", "State", "Constituency", "Candidate", "Party", "EVM Votes", "Postal Votes", "Total Votes", "% of Votes"]

# Convert JSON data to DataFrame
df = pd.DataFrame(all_table_data, columns=columns)

# Convert the specified columns to numeric format
numeric_columns = ["S.N.", "EVM Votes", "Postal Votes", "Total Votes", "% of Votes"]
df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

# Write DataFrame to Excel file
df.to_excel(file_path, index=False, sheet_name='Sheet 1')

print(f"Data written to {file_path}")
