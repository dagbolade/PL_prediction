import requests
import json
import time

def fetch_wta_doubles_matches(player_id, player_full_name, player_country_code):
    """
    Fetches WTA doubles matches information from the API for a given player ID.
    """
    # Define the URL to fetch data from (adjust as needed)
    url = f"https://api.wtatennis.com/tennis/players/{player_id}/matches/?page=0&pageSize=200&id={player_id}&year=&sort=desc&tournamentGroupId="
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
        print(f"Response status code: {response.status_code}")

        # Check if response is successful
        if response.status_code == 200:
            try:
                data = response.json()

                if 'matches' in data:
                    matches = data['matches']
                    all_matches_info = []

                    for match in matches:
                        # Safely access and handle None values
                        opponent = match.get('opponent')
                        opponent_partner = match.get('opponent_partner')
                        partner = match.get('partner')
                        tournament = match.get('tournament')

                        if not opponent or not opponent_partner or not tournament:
                            print(f"Skipping match due to missing opponent, opponent partner, or tournament info: {match}")
                            continue

                        winner = match.get('winner', 0)
                        team_name_1 = match.get('team_name_1', '')
                        team_name_2 = match.get('team_name_2', '')

                        if winner == 1:
                            winner_name = team_name_1
                        elif winner == 2:
                            winner_name = team_name_2
                        else:
                            winner_name = 'Tie or Retired'

                        indoor = tournament.get('inOutdoor', 'Unknown')
                        if indoor == '0':
                            indoor = 'Outdoor'
                        elif indoor == '1':
                            indoor = 'Indoor'
                        else:
                            indoor = 'Unknown'

                        scores = match.get('scores', 'Not Available')

                        match_info = {
                            'PlayerId': player_id,
                            'PlayerFirstName': partner.get('firstName', None),
                            'PlayerLastName': partner.get('lastName', None),
                            'PlayersPartner': partner.get('fullName', None),
                            'PlayerCountryCode': partner.get('countryCode', None),
                            'PlayerDateOfBirth': partner.get('dateOfBirth', None),
                            'playersPartnerId': partner.get('id', 0),
                            'OpponentId': opponent.get('id', 0),
                            'OpponentFirstName': opponent.get('firstName', None),
                            'OpponentLastName': opponent.get('lastName', None),
                            'OpponentFullName': opponent.get('fullName', None),
                            'OpponentCountryCode': opponent.get('countryCode', None),
                            'OpponentDateOfBirth': opponent.get('dateOfBirth', None),
                            'OpponentPartnerId': opponent_partner.get('id', 0),
                            'OpponentPartnerFirstName': opponent_partner.get('firstName', None),
                            'OpponentPartnerLastName': opponent_partner.get('lastName', None),
                            'OpponentPartnerFullName': opponent_partner.get('fullName', None),
                            'OpponentPartnerCountryCode': opponent_partner.get('countryCode', None),
                            'OpponentPartnerDateOfBirth': opponent_partner.get('dateOfBirth', None),
                            'TournamentType': match.get('TournamentType', 'Unknown'),
                            'IndoorOutdoor': indoor,
                            'TournamentName': match.get('TournamentName', 'Unknown'),
                            'TournamentYear': tournament.get('year', 0),
                            'TournamentRoundName': match.get('round_name', 'Unknown'),
                            'TournamentRound': match.get('tourn_round', 'Unknown'),
                            'TournamentStartDate': tournament.get('startDate', None),
                            'TournamentEndDate': tournament.get('endDate', None),
                            'TournamentSurface': tournament.get('surface', None),
                            'TournamentLevel': tournament.get('tournamentGroup', {}).get('level', 'Unknown'),
                            'TournamentCountry': tournament.get('country', None),
                            'TournamentCity': tournament.get('city', None),
                            'PrizeMoney': tournament.get('prizeMoney', 0),
                            'PrizeMoneyCurrency': tournament.get('prizeMoneyCurrency', None),
                            'Winner': winner,
                            'WinnerName': winner_name,
                            'RoundName': match.get('round_name', 'Unknown'),
                            'Scores': scores
                        }

                        all_matches_info.append(match_info)

                    # Save doubles matches information to a JSON file named after the player
                    save_to_json(all_matches_info, f'{player_full_name}_doubles_matches.json')
                    print(f"Doubles matches information saved to {player_full_name}_doubles_matches.json")

                else:
                    print(f"No matches found for Player ID: {player_id}")
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

def save_to_json(data, filename):
    """
    Saves data to a JSON file.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Data saved to {filename}")

def main():
    try:
        # Load the player IDs and names from the JSON file
        with open('wta_doubles_players_info.json', 'r', encoding='utf-8') as file:
            players_info = json.load(file)

        # Process each player
        for player in players_info:
            if 'Id' not in player or 'FullName' not in player or 'CountryCode' not in player:
                print(f"Skipping player due to missing required information: {player}")
                continue

            player_id = player['Id']
            player_full_name = player['FullName']
            player_country_code = player['CountryCode']

            print(f"Fetching doubles matches for {player_full_name}...")
            fetch_wta_doubles_matches(player_id, player_full_name, player_country_code)

            # Introduce a delay to the server
            time.sleep(3)  # Adjust delay as needed

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
