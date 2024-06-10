import requests
from bs4 import BeautifulSoup
import json
import os

# URL of the page to be scraped
url = "https://results.eci.gov.in/PcResultGenJune2024/ConstituencywiseS018.htm"

# Make a request to the website
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Print the HTML content of the page for debugging
    html_content = response.content
    print(html_content)  # Uncomment this to see the raw HTML content

    # Parse the HTML content of the page
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the table containing the data
    table = soup.find('table')  # Start with finding any table

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
                table_data.append(cols)
    else:
        print("Table not found")
else:
    print("Failed to retrieve the page")

# Convert the table data to JSON
table_data_json = json.dumps(table_data, indent=4)

# Determine the path to the desktop
desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')

# Create the file path for the JSON file on the desktop
json_file_path = os.path.join(desktop_path, 'table_data.json')

# Save the JSON data to a file on the desktop
with open(json_file_path, 'w') as json_file:
    json_file.write(table_data_json)  # Newly added line

print(f"Table data has been saved to {json_file_path}")  # Newly added line
