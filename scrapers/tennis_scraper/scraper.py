import os
from urllib.parse import urljoin
import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
from pathlib import Path

def scrape_country_links(html_content, base_url, headers, skip_urls):
    soup = BeautifulSoup(html_content, 'html.parser')
    time.sleep(3)

    # Extract country links from the table
    country_links = []
    for row in soup.find_all('tr'):
        link_tag = row.find('a', href=True)
        if link_tag:
            country_link = link_tag['href']
            full_country_link = urljoin(base_url, country_link)

            if any(skip_url in full_country_link for skip_url in skip_urls):
                continue

            country_links.append(full_country_link)

    unique_country_links = set(country_links)
    print(unique_country_links)
    return unique_country_links

def scrape_page_for_files(page_url, base_url, directory_name):
    response = requests.get(page_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a', href=True):
            if link['href'].endswith(('.csv', '.txt', '.xls', '.xlsx')):
                file_url = urljoin(base_url, link['href'])
                download_file(file_url, directory_name)
    else:
        print(f"Failed to retrieve page from {page_url}. Status code: {response.status_code}")



def get_directory_name(link_text):
    # Return a directory name based on the link text
    if "ATP Men's Tour" in link_text:
        return "ATP_Mens_Tour"
    elif "WTA Women's Tour" in link_text:
        return "WTA_Womens_Tour"
    else:
        return link_text.replace(' ', '_')


def download_file(file_url, directory_name):
    response = requests.get(file_url, stream=True)
    if response.status_code == 200:
        # Extract year and filename from the URL
        parts = file_url.split('/')
        year = parts[-2]  # The year is the second last part of the URL
        filename = parts[-1]  # The filename is the last part of the URL

        # Prepend year to the filename
        new_filename = f"{year}_{filename}"
        file_path = os.path.join(directory_name, new_filename)

        # Ensure the directory exists
        os.makedirs(directory_name, exist_ok=True)

        # Write the file to the directory
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Saved {new_filename} to {directory_name}")
    else:
        print(f"Failed to retrieve file from {file_url}. Status code: {response.status_code}")


def download_files_from_csv(csv_file_path, base_url):
    df = pd.read_csv(csv_file_path)
    for index, row in df.iterrows():
        link = row['Links']
        # The directory name should be derived from the link. This is placeholder logic.
        directory_name = link.split('/')[-1].split('.')[0]  # This assumes the filename is useful as a directory name
        if link.endswith(('.csv', '.txt', '.xls', '.xlsx')):
            file_url = urljoin(base_url, link)
            download_file(file_url, directory_name)
        else:
            # Here we should scrape the page for files
            directory_name = link.split('/')[-1].split('.')[0]  # Adjust this as needed
            scrape_page_for_files(link, base_url, directory_name)

def main():
    url = 'http://www.tennis-data.co.uk/data.php'
    base_url = 'http://www.tennis-data.co.uk/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }
    skip_urls = []  # Define any URLs you wish to skip
    csv_file_path = 'tennis_links.csv'

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html_content = response.content
        country_links = scrape_country_links(html_content, base_url, headers, skip_urls)
        print(country_links)
        # save to CSV
        link_df = pd.DataFrame(list(country_links), columns=['Links'])
        link_df.to_csv(csv_file_path, index=False)
        print("Links have been saved to csv")
    else:
        print(f"Failed to retrieve page, status code: {response.status_code}")

    # After saving links to tennis_links.csv, proceed to download the files
    download_files_from_csv(csv_file_path, base_url)

if __name__ == "__main__":
    main()

