import requests
from bs4 import BeautifulSoup

# Base URL of anime1.me
base_url = 'https://anime1.me'

# Send a request to the URL
response = requests.get(base_url)
response.encoding = 'utf-8'

# Parse the response content with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find all rows in the table with anime information
rows = soup.find_all('tr', class_='sorting')

for row in rows:
    # Extract title
    title_tag = row.find('td', class_='sorting')
    title = title_tag.text.strip() if title_tag else 'No title'

    # Extract year
    year_tag = row.find('td', class_='sorting sorting_asc')
    year = year_tag.text.strip() if year_tag else 'No year'

    # Print the information
    print(f'Title: {title}')
    print(f'Year: {year}')
    print('---')

# Note: You may need to handle pagination or additional pages for complete data.
