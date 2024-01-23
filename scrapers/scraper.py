from bs4 import BeautifulSoup
import requests
import pandas as pd
from urllib.parse import urljoin
import time
import re


def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename)


def scrape_country_links(html_content, base_url, headers, skip_urls):
    soup = BeautifulSoup(html_content, 'html.parser')
    time.sleep(3)

    # Extract country links from the table
    country_links = []
    for row in soup.find_all('tr'):
        link_tag = row.find('a', href=True)
        if link_tag:
            country_link = link_tag['href']
            full_country_link = urljoin(base_url, country_link)  # Construct the complete URL

            # Skip if the URL contains any of the specified strings
            if any(skip_url in full_country_link for skip_url in skip_urls):
                continue

            country_links.append(full_country_link)

    unique_country_links = set(country_links)
    print(unique_country_links)
    return unique_country_links


def scrape_country_names(country_link, base_url, headers, skip_urls):
    country_url = urljoin(base_url, country_link)

    # Skip requests if the URL contains any of the specified strings
    if any(skip_url in country_url for skip_url in skip_urls):
        print(f'Skipping {country_url}')
        return

    response = requests.get(country_url, headers=headers)
    time.sleep(3)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True)]

        sanitized_filename = sanitize_filename(country_link)
        df_links = pd.DataFrame({'Links': links})
        df_links.to_csv(f'{sanitized_filename}_link.csv', index=False)
    else:
        print(f'Failed to retrieve HTML content from {country_url}. Status code: {response.status_code}')


def main():
    url = 'https://www.football-data.co.uk/data.php'
    base_url = 'https://www.football-data.co.uk/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }
    # Skip this URL when scraping country links
    skip_urls = ['https://www.accastats.com/', 'www.bettingadvice.com']

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html_content = response.content
        country_links = scrape_country_links(html_content, base_url, headers, skip_urls)

        country_data = []
        for country_link in country_links:
            scrape_country_names(country_link, base_url, headers, skip_urls)
            print(f'Links crawled for {country_link}')
            country_data.append({'CountryLink': country_link})

        cleaned_country_links = [link.split(base_url)[-1] for link in country_links]

        df = pd.DataFrame({'CountryLink': cleaned_country_links})
        df.to_csv('country_data.csv', index=False)
    else:
        print(f'Failed to retrieve HTML content from {url}. Status code: {response.status_code}')


if __name__ == "__main__":
    main()
