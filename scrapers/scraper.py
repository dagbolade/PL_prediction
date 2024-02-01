import os
from bs4 import BeautifulSoup
import requests
import pandas as pd
from urllib.parse import urljoin
import time
import re
from pathlib import Path

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

        # Strip base_url from country_link
        stripped_country_link = country_link.replace(base_url, '')

        # Sanitize filename to prevent errors when saving
        sanitized_filename = sanitize_filename(stripped_country_link)
        # Save the links to a CSV file
        df_links = pd.DataFrame({'Links': links})
        df_links.to_csv(f'{sanitized_filename}_link.csv', index=False)
        print(f'Saved {len(links)} links to {sanitized_filename}_link.csv')
    else:
        print(f'Failed to retrieve HTML content from {country_url}. Status code: {response.status_code}')

def download_and_save_file(link, directory_path, file_extension, base_url):
    # Ensuring the link is complete
    if not link.startswith('http'):
        link = urljoin(base_url, link)

    response = requests.get(link)
    time.sleep(3)

    if response.status_code == 200:
        file_name = os.path.basename(link)
        file_path = os.path.join(directory_path, file_name)
        with open(file_path, 'wb') as file:
            file.write(response.content)

        print(f'Downloaded and saved {file_extension} to {file_path}')
        return file_path
    else:
        print(f'Failed to download {file_extension} from {link}. Status code: {response.status_code}')
        return None


def download_file(link, directory_path):
    # Get the last part of the link to use as filename
    filename = link.split('/')[-1]

    # Filter out files that are not .csv or .txt
    if not (filename.endswith('.csv') or filename.endswith('.txt')):
        print(f'Skipping non-csv/txt file: {filename}')
        return

    # Create a Path object for the file
    file_path = Path(directory_path) / filename

    # If the file already exists, append a number to the filename
    if file_path.exists():
        counter = 1
        while True:
            new_file_path = Path(directory_path) / f"{file_path.stem}_{counter}{file_path.suffix}"
            if not new_file_path.exists():
                file_path = new_file_path
                break
            counter += 1

    # Download and save the file
    response = requests.get(link)
    if response.status_code == 200:
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f'Downloaded and saved: {file_path.name}')
    else:
        print(f'Error downloading {link}: Status code {response.status_code}')

def scrape_links_from_csv(csv_file_path):
    base_url = 'https://www.football-data.co.uk/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }

    df = pd.read_csv(csv_file_path)
    links = df['Links'].dropna().unique()

    # Filter links from 'notes.txt' to 'contact.php'
    relevant_links = [link for link in links if 'notes.txt' <= link <= 'contact.php']

    for link in relevant_links:
        print(f'Scraping link: {link}')
        response = requests.get(link, headers=headers)
        time.sleep(3)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = [a['href'] for a in soup.find_all('a', href=True)]

            # Create a directory with the CSV file's name
            directory_name = os.path.splitext(os.path.basename(link))[0]
            directory_path = os.path.join(os.getcwd(), directory_name)
            os.makedirs(directory_path, exist_ok=True)

            # Download and save the CSV file
            csv_path = download_and_save_file(link, directory_path, 'csv')

            # Download and save the notes.txt file
            notes_path = download_and_save_file('https://www.football-data.co.uk/notes.txt', directory_path, 'notes.txt')


# Function to sanitize and create directory names
def create_directory_from_csv(csv_file_name):
    # Remove extension and any non-directory-friendly characters
    directory_name = sanitize_filename(csv_file_name.replace('.csv', ''))
    directory_path = os.path.join(os.getcwd(), directory_name)
    if not os.path.exists(directory_path):
        os.makedirs(directory_path, exist_ok=True)
    return directory_path


def process_country_csv(csv_file_path, base_url):
    # Create directory named after the CSV file (excluding the extension)
    directory_name = csv_file_path.split('.')[0]
    directory_path = os.path.join(os.getcwd(), directory_name)
    os.makedirs(directory_path, exist_ok=True)

    # Read the "index" CSV file that contains links to other CSV files
    df = pd.read_csv(csv_file_path)
    for link in df['Links']:
        # Convert link to string, avoiding TypeError
        link = str(link)
        # Construct the full URL for each file
        full_url = base_url + link
        download_file(full_url, directory_path)

# Function to scrape all CSV files in a directory
def scrape_all_csv_files(directory, base_url):
    for filename in os.listdir(directory):
        if filename.endswith('.csv') and filename != 'country_data.csv':
            csv_file_path = os.path.join(directory, filename)
            process_country_csv(csv_file_path, base_url)




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

        # Call the function to scrape links from CSV files
        base_url = 'https://www.football-data.co.uk/'
        scrape_all_csv_files(os.getcwd(), base_url)

    else:
        print(f'Failed to retrieve HTML content from {url}. Status code: {response.status_code}')

if __name__ == "__main__":
    main()
