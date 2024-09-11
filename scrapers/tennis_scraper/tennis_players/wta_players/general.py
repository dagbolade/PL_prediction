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


def fetch_wta_player_matches(player_id, player_full_name, player_country_code):
    """
    Fetches WTA player matches information from the API for a given player ID.
    """
    # Define the URL to fetch data from
    url = f"https://api.wtatennis.com/tennis/players/{player_id}/matches/?page=0&pageSize=200&id={player_id}&year=&type=S&sort=desc&tournamentGroupId="
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
                        tournament = match.get('tournament')

                        if not opponent or not tournament:
                            print(f"Skipping match due to missing opponent or tournament info: {match}")
                            continue

                        winner = match.get('winner', 0)
                        team_name_1 = match.get('team_name_1', '')
                        team_name_2 = match.get('team_name_2', '')

                        if winner == 1:
                            winner_name = team_name_1.split(player_country_code)[0].strip()
                        elif winner == 2:
                            winner_name = team_name_2.split(player_country_code)[0].strip()
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
                            'OpponentId': opponent.get('id', 0),
                            'OpponentFirstName': opponent.get('firstName', None),
                            'OpponentLastName': opponent.get('lastName', None),
                            'PlayersRank': match.get('rank_1', 0),
                            'OpponentsRank': match.get('rank_2', 0),
                            'OpponentFullName': opponent.get('fullName', None),
                            'OpponentCountryCode': opponent.get('countryCode', None),
                            'OpponentDateOfBirth': opponent.get('dateOfBirth', None),
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

                    # Save player matches information to a JSON file named after the player
                    save_to_json(all_matches_info, f'{player_full_name}_singles_matches.json')
                    print(f"Player matches information saved to {player_full_name}_singles_matches.json")

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
        # Fetch singles player info
        print("Fetching singles player info...")
        singles_players_info = fetch_wta_player_info('singles')

        # Fetch doubles player info
        print("Fetching doubles player info...")
        doubles_players_info = fetch_wta_player_info('doubles')

        if singles_players_info:
            # Process singles players
            for player in singles_players_info:
                player_id = player['Id']
                player_full_name = player['FullName']
                player_country_code = player['CountryCode']

                print(f"Fetching singles stats for {player_full_name}...")
                fetch_player_stats(player_id, player_full_name, player_country_code)

                print(f"Fetching singles matches for {player_full_name}...")
                fetch_wta_player_matches(player_id, player_full_name, player_country_code)

                # Introduce a delay to the server
                time.sleep(3)  # Adjust delay as needed

        if doubles_players_info:
            # Process doubles players
            for player in doubles_players_info:
                player_id = player['Id']
                player_full_name = player['FullName']
                player_country_code = player['CountryCode']

                print(f"Fetching doubles stats for {player_full_name}...")
                fetch_player_stats(player_id, player_full_name, player_country_code)

                print(f"Fetching doubles matches for {player_full_name}...")
                fetch_wta_doubles_matches(player_id, player_full_name, player_country_code)

                # Introduce a delay to the server
                time.sleep(5)  # Adjust delay as needed

    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
