import requests
import json
import time


def fetch_wta_player_info(endpoint):
    """
    Fetches WTA player information from the given API endpoint.
    """
    if endpoint == 'singles':
        url = "https://api.wtatennis.com/tennis/players/ranked?page=0&pageSize=200&type=rankSingles&sort=asc&name=&metric=SINGLES&at=2024-07-08&nationality="
    elif endpoint == 'doubles':
        url = "https://api.wtatennis.com/tennis/players/ranked?page=0&pageSize=200&type=rankDoubles&sort=asc&name=&metric=DOUBLES&at=2024-07-08&nationality="
    else:
        raise ValueError("Invalid endpoint. Supported endpoints: 'singles', 'doubles'")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json'
    }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            all_players_info = []

            for player_entry in data:
                player_data = player_entry['player']

                player_info = {
                    'Id': player_data.get('id', ''),
                    'FirstName': player_data.get('firstName', ''),
                    'LastName': player_data.get('lastName', ''),
                    'FullName': player_data.get('fullName', ''),
                    'CountryCode': player_data.get('countryCode', ''),
                    'DateOfBirth': player_data.get('dateOfBirth', ''),
                    'Ranking': player_entry.get('ranking', ''),
                    'Points': player_entry.get('points', ''),
                    'TournamentsPlayed': player_entry.get('tournamentsPlayed', ''),
                    'Movement': player_entry.get('movement', ''),
                    'RankedAt': player_entry.get('rankedAt', '')
                }

                all_players_info.append(player_info)

            return all_players_info

        else:
            print(f"Failed to fetch data from {url}. Status code: {response.status_code}")
            return None

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


def save_to_json(data, filename):
    """
    Saves data to a JSON file.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Data saved to {filename}")


def main():
    try:
        # Fetch WTA singles player information
        print("Fetching WTA singles player information...")
        wta_singles_players_info = fetch_wta_player_info('singles')

        if wta_singles_players_info:
            # Save singles player information to a JSON file
            save_to_json(wta_singles_players_info, 'wta_singles_players_info.json')
            print("WTA singles player information saved to wta_singles_players_info.json")

        # Fetch WTA doubles player information
        print("Fetching WTA doubles player information...")
        wta_doubles_players_info = fetch_wta_player_info('doubles')

        if wta_doubles_players_info:
            # Save doubles player information to a JSON file
            save_to_json(wta_doubles_players_info, 'wta_doubles_players_info.json')
            print("WTA doubles player information saved to wta_doubles_players_info.json")

    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
