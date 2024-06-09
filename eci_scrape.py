import requests
from bs4 import BeautifulSoup

# URL of the page to be scraped
url = "https://results.eci.gov.in/PcResultGenJune2024/candidateswise-S018.htm"

# Make a request to the website
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table containing the data
    table = soup.find('table', {'class': 'table-party'})

    # Check if the table exists
    if table:
        # Iterate through the rows of the table
        for row in table.find_all('tr'):
            # Extract the columns
            cols = row.find_all('td')
            # Get the text from each column and print it
            if cols:
                cols = [col.text.strip() for col in cols] #smaple change
                print(cols)
    else:
        print("Table not found")
else:
    print("Failed to retrieve the page")
