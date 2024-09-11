import requests
import json


def fetch_wta_player_matches(player_id):
    """
    Fetches WTA player matches information from the API for a given player ID.
    """
    url = f"https://api.wtatennis.com/tennis/players/{player_id}/matches/?page=0&pageSize=10&id={player_id}&year=&type=S&sort=desc&tournamentGroupId="

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json'
    }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if 'matches' in data:
                all_matches_info = []

                for match in data['matches']:
                    winner = match['winner']
                    if winner == 1:
                        winner_name = match['team_name_1']
                    elif winner == 2:
                        winner_name = match['team_name_2']
                    else:
                        winner_name = "Tie or Retired"

                    match_info = {
                        'PlayerId': player_id,
                        'OpponentId': match['opponent']['id'],
                        'OpponentCountry': match['Country'],
                        'OpponentFirstName': match['opponent']['firstName'],
                        'OpponentLastName': match['opponent']['lastName'],
                        'OpponentFullName': match['opponent']['fullName'],
                        'OpponentCountryCode': match['opponent']['countryCode'],
                        'OpponentDateOfBirth': match['opponent']['dateOfBirth'],
                        'TournamentName': match['tournament']['title'],
                        'TournamentYear': match['tournament']['year'],
                        'TournamentStartDate': match['tournament']['startDate'],
                        'TournamentEndDate': match['tournament']['endDate'],
                        'TournamentSurface': match['tournament']['surface'],
                        'TournamentLevel': match['tournament']['tournamentGroup']['level'],
                        'TournamentCountry': match['tournament']['country'],
                        'PrizeMoney': match['PrizeMoney'],
                        'PrizeMoneyCurrency': match['tournament']['prizeMoneyCurrency'],
                        'Winner': winner,
                        'WinnerName': winner_name,
                        'RoundName': match['round_name'],
                        'Scores': match['scores'],
                        'StartDate': match['StartDate']
                    }

                    all_matches_info.append(match_info)

                return all_matches_info
            else:
                print(f"No matches found for Player ID: {player_id}")
                return []

        else:
            print(f"Failed to fetch data from {url}. Status code: {response.status_code}")
            return None

    except Exception as e:
        print(f"An error occurred while fetching matches for Player ID {player_id}: {str(e)}")
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
        # Example player ID to fetch matches
        player_id = 317964

        print(f"Fetching WTA player matches for Player ID: {player_id}...")
        wta_player_matches_info = fetch_wta_player_matches(player_id)

        if wta_player_matches_info is not None:
            # Save player matches information to a JSON file
            save_to_json(wta_player_matches_info, f'wta_player_matches_{player_id}.json')
            print(f"WTA player matches information saved to wta_player_matches_{player_id}.json")

    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
