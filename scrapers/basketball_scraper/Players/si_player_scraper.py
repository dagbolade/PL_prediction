import csv
import requests

def si_nba_scraper():
    base_url = 'https://uswidgets.fn.sportradar.com/sportradarmlb/en_us/Etc:UTC/gismo/stats_season_playerstats/106289/main/-1/-1/1'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept': 'application/json'
    }
    try:
        response = requests.get(base_url, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON content
            json_data = response.json()
            # Access the players data
            players_data = json_data.get('doc', [])[0].get('data', {}).get('players', {})

            # Open a CSV file in write mode
            with open('si_scraper_data.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                # Write the header row based on the option
                writer.writerow([
                    "Name",
                    "Team",
                    "Position",
                    "Points",
                    "Assists",
                    "Minutes",
                    "Field Goals Made",
                    "Field Goals Attempted",
                    "Field Goal Percentage",
                    "Three Points Made",
                    "Three Points Attempted",
                    "Three Point Percentage",
                    "Two Point Percentage",
                    "Free Throws Made",
                    "Free Throws Attempted",
                    "Free Throw Percentage",
                    "Rebounds",
                    "Turnovers",
                    "Steals",
                    "Blocks",
                    "Personal Fouls",
                    "Points per Match",
                    "Turnovers per Match",
                    "Free Throws Attempted per Match",
                    "Field Goals Attempted per Match",
                    "Assists per Match",
                    "Blocks per Match",
                    "Personal Fouls per Match",
                    "Rebounds per Match",
                    "Three Points Made per Match",
                    "Free Throws Made per Match",
                    "Field Goals Made per Match",
                    "Steals per Match",
                    "Three Points Attempted per Match",
                    "Games Played"
                ])

                # Iterate over the players and extract the required data
                for player_id, player_info in players_data.items():
                    name = player_info.get('name', '')
                    position = player_info.get('position', {}).get('name', '')
                    points = player_info.get('stats', {}).get('points', {}).get('value', '')
                    assists = player_info.get('stats', {}).get('assists', {}).get('value', '')
                    minutes = player_info.get('stats', {}).get('minutes', {}).get('value', '')
                    field_goals_made = player_info.get('stats', {}).get('field_goals_made', {}).get('value', '')
                    field_goals_attempted = player_info.get('stats', {}).get('field_goals_attempted', {}).get('value', '')
                    field_goal_percentage = player_info.get('stats', {}).get('field_goals_percentage', {}).get('value', '')
                    three_points_made = player_info.get('stats', {}).get('three_points_made', {}).get('value', '')
                    three_points_attempted = player_info.get('stats', {}).get('three_points_attempted', {}).get('value', '')
                    three_point_percentage = player_info.get('stats', {}).get('three_points_percentage', {}).get('value', '')
                    two_point_percentage = player_info.get('stats', {}).get('two_points_percentage', {}).get('value', '')
                    free_throws_made = player_info.get('stats', {}).get('free_throws_made', {}).get('value', '')
                    free_throws_attempted = player_info.get('stats', {}).get('free_throws_attempted', {}).get('value', '')
                    free_throw_percentage = player_info.get('stats', {}).get('free_throws_percentage', {}).get('value', '')
                    rebounds = player_info.get('stats', {}).get('rebounds', {}).get('value', '')
                    turnovers = player_info.get('stats', {}).get('turnovers', {}).get('value', '')
                    steals = player_info.get('stats', {}).get('steals', {}).get('value', '')
                    blocks = player_info.get('stats', {}).get('blocks', {}).get('value', '')
                    personal_fouls = player_info.get('stats', {}).get('personal_fouls', {}).get('value', '')
                    points_per_match = player_info.get('stats', {}).get('points_per_match', {}).get('value', '')
                    turnovers_per_match = player_info.get('stats', {}).get('turnovers_per_match', {}).get('value', '')
                    free_throws_attempted_per_match = player_info.get('stats', {}).get('free_throws_attempted_per_match', {}).get('value', '')
                    field_goals_attempted_per_match = player_info.get('stats', {}).get('field_goals_attempted_per_match', {}).get('value', '')
                    assists_per_match = player_info.get('stats', {}).get('assists_per_match', {}).get('value', '')
                    blocks_per_match = player_info.get('stats', {}).get('blocks_per_match', {}).get('value', '')
                    personal_fouls_per_match = player_info.get('stats', {}).get('personal_fouls_per_match', {}).get('value', '')
                    rebounds_per_match = player_info.get('stats', {}).get('rebounds_per_match', {}).get('value', '')
                    three_points_made_per_match = player_info.get('stats', {}).get('three_points_made_per_match', {}).get('value', '')
                    free_throws_made_per_match = player_info.get('stats', {}).get('free_throws_made_per_match', {}).get('value', '')
                    field_goals_made_per_match = player_info.get('stats', {}).get('field_goals_made_per_match', {}).get('value', '')
                    steals_per_match = player_info.get('stats', {}).get('steals_per_match', {}).get('value', '')
                    three_points_attempted_per_match = player_info.get('stats', {}).get('three_points_attempted_per_match', {}).get('value', '')
                    games_played = player_info.get('stats', {}).get('games_played', {}).get('value', '')

                    # Write the row to the CSV file
                    writer.writerow([
                        name, position, points, assists, minutes, field_goals_made, field_goals_attempted,
                        field_goal_percentage, three_points_made, three_points_attempted, three_point_percentage,
                        two_point_percentage, free_throws_made, free_throws_attempted, free_throw_percentage,
                        rebounds, turnovers, steals, blocks, personal_fouls, points_per_match, turnovers_per_match,
                        free_throws_attempted_per_match, field_goals_attempted_per_match, assists_per_match,
                        blocks_per_match, personal_fouls_per_match, rebounds_per_match, three_points_made_per_match,
                        free_throws_made_per_match, field_goals_made_per_match, steals_per_match,
                        three_points_attempted_per_match, games_played
                    ])

            print("Data has been saved to 'si_scraper_data.csv' file.")

        else:
            print("Failed to fetch data from the website.")
    except Exception as e:
        print("An error occurred:", str(e))

si_nba_scraper()
