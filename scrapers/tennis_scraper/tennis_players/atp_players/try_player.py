import requests
import pandas as pd
import json
import time
from fake_useragent import UserAgent

ua = UserAgent()

def fetch_player_info(player_id):
    """
    Fetches comprehensive player information using player ID from ATP Tour website.
    """
    player_profile_url = f'https://www.atptour.com/en/-/www/players/hero/{player_id}?v=1'

    headers = {
        'User-Agent': ua.random,
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'https://www.google.com/'
    }
    response = requests.get(player_profile_url, headers=headers)

    if response.status_code == 200:
        player_data = response.json()

        # Optionally, you can parse and filter data here as needed
        return player_data
    else:
        raise Exception(f"Failed to fetch data from {player_profile_url}. Status code: {response.status_code}")

def save_to_json(data, filename):
    """
    Saves data to a JSON file.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Data saved to {filename}")

def main():
    try:
        # Read player data from both CSV files
        players_df_doubles = pd.read_csv('players_info_doubles.csv')
        players_df_singles = pd.read_csv('players_info_singles.csv')

        # List to hold all player information
        all_players_info = []

        # Process players from doubles data
        for idx, player_row in players_df_doubles.iterrows():
            player_id = player_row['PlayerId']
            player_name = player_row['Name']

            print(f"Fetching player info for {player_name}...")
            player_info = fetch_player_info(player_id)

            # Add player name to the info
            player_info['Name'] = player_name

            all_players_info.append(player_info)

            # Print player info
            print(json.dumps(player_info, indent=4))

            time.sleep(3)  # Introduce a delay to be polite

        # Process players from singles data
        for idx, player_row in players_df_singles.iterrows():
            player_id = player_row['PlayerId']
            player_name = player_row['Name']

            print(f"Fetching player info for {player_name}...")
            player_info = fetch_player_info(player_id)

            # Add player name to the info
            player_info['Name'] = player_name

            all_players_info.append(player_info)

            # Print player info
            print(json.dumps(player_info, indent=4))

            time.sleep(3)  # Introduce a delay to be polite

        # Save all player information to a single JSON file
        save_to_json(all_players_info, 'all_players_info.json')

        print("Player information saved to all_players_info.json")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
