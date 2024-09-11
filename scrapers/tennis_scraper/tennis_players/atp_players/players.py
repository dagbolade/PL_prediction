import requests
import pandas as pd
import time
from fake_useragent import UserAgent

ua = UserAgent()


def fetch_data(url):
    """
    Fetches JSON data from the given URL.
    """
    headers = {
        'User-Agent': ua.random,
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'https://www.google.com/'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data from {url}. Status code: {response.status_code}")


def extract_player_data(players_data):
    """
    Extracts required player information from the data.
    """
    extracted_data = []
    for player in players_data:
        player_data = {
            'Rank': player['RankNo'],
            'Name': player['Name'],
            'Points': player['Points'],
            'Country': player['Country'],
            'PlayerId': player['PlayerId'],
            'PlayerProfileUrl': f"https://www.atptour.com{player['PlayerProfileUrl']}"
        }
        extracted_data.append(player_data)
    return extracted_data


def save_to_csv(data, filename):
    """
    Saves data to a CSV file.
    """
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")


def scrape_and_save(url, filename):
    """
    Scrapes player data from the given URL and saves it to CSV.
    """
    try:
        data = fetch_data(url)
        players_data = extract_player_data(data)
        save_to_csv(players_data, filename)
    except Exception as e:
        print(f"An error occurred while processing {url}: {e}")


def main():
    """
    Main function to orchestrate the scraping process.
    """
    try:
        # Define URLs for singles and doubles
        singles_url = 'https://www.atptour.com/en/-/www/rank/sglroll/100?v=1'
        doubles_url = 'https://www.atptour.com/en/-/www/rank/dblroll/100?v=1'

        # Scrape and save singles data
        scrape_and_save(singles_url, 'players_info_singles.csv')
        time.sleep(3)  # Introduce a delay

        # Scrape and save doubles data
        scrape_and_save(doubles_url, 'players_info_doubles.csv')
    except Exception as e:
        print(f"An error occurred during scraping: {e}")


if __name__ == "__main__":
    main()
