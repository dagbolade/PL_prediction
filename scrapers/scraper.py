from bs4 import BeautifulSoup
import requests
import pandas as pd
from urllib.parse import urljoin
import time
import re


def sanitize_filename(filename):
    # Replace invalid characters with underscores
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def scrape_country_links(html_content, base_url, headers):
    soup = BeautifulSoup(html_content, 'html.parser')
    time.sleep(3)

    # Extract country links from the table
    country_links = []
    for row in soup.find_all('tr'):
        link_tag = row.find('a', href=True)
        if link_tag:
            country_link = link_tag['href']
            full_country_link = urljoin(base_url, country_link)  # Construct the complete URL
            country_links.append(full_country_link)

    # Use a set to store unique country links
    unique_country_links = set(country_links)
    print(unique_country_links)
    return unique_country_links


# Function to scrape country names from the given country link
def scrape_country_names(country_link, base_url,  headers):
    country_url = urljoin(base_url, country_link)
    response = requests.get(country_url, headers=headers)
    time.sleep(3)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract links from <a> tags
        links = [a['href'] for a in soup.find_all('a', href=True)]

        # Save the links to a new CSV file with sanitized filename
        sanitized_filename = sanitize_filename(country_link)
        df_links = pd.DataFrame({'Links': links})
        df_links.to_csv(f'{sanitized_filename}_link.csv', index=False)

    else:
        print(f'Failed to retrieve HTML content from {country_url}. Status code: {response.status_code}')


def main():
    # Website to scrape
    url = 'https://www.football-data.co.uk/data.php'
    base_url = 'https://www.football-data.co.uk/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }

    # Step 1: Fetch HTML content
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html_content = response.content

        # Step 2: Scrape unique country links
        country_links = scrape_country_links(html_content, base_url, headers)

        # Step 3: Loop through country links and scrape country names
        country_data = []
        for country_link in country_links:
            # This function does not extract country names
            scrape_country_names(country_link, base_url, headers)

            # Print or further process the scraped country names (which is now an empty list)
            print(f'Links crawled for {country_link}')

            # Save country link to a list
            country_data.append({'CountryLink': country_link})

        # Clean up country links before saving to CSV
        cleaned_country_links = [link.split(base_url)[-1] for link in country_links]

        # Convert the list to a DataFrame and save to CSV
        df = pd.DataFrame({'CountryLink': cleaned_country_links})
        df.to_csv('country_data.csv', index=False)
    else:
        print(f'Failed to retrieve HTML content from {url}. Status code: {response.status_code}')


if __name__ == "__main__":
    main()
