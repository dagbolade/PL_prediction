import requests
import json
import time

def fetch_player_stats(player_id, player_full_name, player_country_code):
    """
    Fetches player statistics for a given player ID and year from the WTA API.
    """
    base_url = f"https://api.wtatennis.com/tennis/players/{player_id}/year/"
    years = [2024, 2023, 2022]
    all_stats = []

    for year in years:
        url = f"{base_url}{year}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'https://www.wtatennis.com/'
        }

        try:
            # Send request
            response = requests.get(url, headers=headers)
            print(f"Response status code for {player_full_name} - {year}: {response.status_code}")

            # Check if response is successful
            if response.status_code == 200:
                try:
                    data = response.json()

                    if 'stats' in data and 'player' in data:
                        player_stats = {
                            'PlayerId': player_id,
                            'FullName': player_full_name,
                            'CountryCode': player_country_code,
                            'Stats': data['stats']
                        }
                        all_stats.append(player_stats)

                    else:
                        print(f"No stats found for {player_full_name} - {year}")
                        print(f"Response content: {data}")

                except json.JSONDecodeError as je:
                    print(f"Error decoding JSON: {str(je)}")
                    print(f"Response content: {response.text}")

            else:
                print(f"Failed to fetch data from {url}. Status code: {response.status_code}")
                print(f"Response content: {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {str(e)}")
            print(f"Failed URL: {url}")

        time.sleep(1)  # Introduce a delay to not overload the server

    return all_stats

def save_to_json(data, filename):
    """
    Saves data to a JSON file.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Data saved to {filename}")

def main():
    try:
        # Load singles players info from JSON file
        with open('wta_singles_players_info.json', 'r', encoding='utf-8') as file:
            singles_players_info = json.load(file)

        # Load doubles players info from JSON file
        with open('wta_doubles_players_info.json', 'r', encoding='utf-8') as file:
            doubles_players_info = json.load(file)

        # Extract unique player names
        singles_player_names = {player['FullName'] for player in singles_players_info}
        doubles_player_names = {player['FullName'] for player in doubles_players_info}

        # Get intersection of unique player names
        unique_player_names = singles_player_names - doubles_player_names

        # Fetch and collect player stats for unique players
        all_stats = []
        for player in singles_players_info:
            player_full_name = player['FullName']
            if player_full_name in unique_player_names:
                player_id = player['Id']
                player_country_code = player['CountryCode']
                stats = fetch_player_stats(player_id, player_full_name, player_country_code)
                all_stats.extend(stats)

        # Save combined stats to a JSON file
        save_to_json(all_stats, 'combined_player_stats.json')

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
