import csv
import requests

def si_scraper():
    base_url = 'https://uswidgets.fn.sportradar.com/sportradarmlb/en_us/Etc:UTC/gismo/stats_season_teamstats/106289/main'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept': 'application/json'
    }

    try:
        response = requests.get(base_url, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON content
            data = response.json()

            # Open a CSV file in write mode
            with open('si_scraper_data.csv', mode='w', newline='') as file:
                writer = csv.writer(file)

                # Write the header row
                writer.writerow(['Team ID', 'Medium Name', 'Name', 'Nickname', 'Minutes', 'Field Goals Made', 'Field Goals Attempted', 'Field Goals Percentage', 'Three Points Made', 'Three Points Attempted', 'Three Points Percentage', 'Two Points Made', 'Two Points Attempted', 'Blocked Attempts', 'Free Throws Made', 'Free Throws Attempted', 'Free Throws Percentage', 'Offensive Rebounds', 'Defensive Rebounds', 'Rebounds', 'Turnovers', 'Steals', 'Blocks', 'Assist Turnover Ratio', 'Personal Fouls', 'Technical Fouls', 'Flagrant Fouls', 'Points', 'Player Technical Fouls', 'Team Rebounds', 'Team Technical Fouls', 'Team Turnovers', 'Foulouts', 'Fast Break Points', 'Paint Points', 'Second Chance Points', 'Points Off Turnovers', 'Ejections', 'Turnovers Per Match', 'Blocks Per Match', 'Steals Per Match', 'Opponent Minutes', 'Opponent Field Goals Made', 'Opponent Field Goals Attempted', 'Opponent Three Points Made', 'Opponent Three Points Attempted', 'Opponent Free Throws Made', 'Opponent Free Throws Attempted', 'Opponent Offensive Rebounds', 'Opponent Defensive Rebounds', 'Opponent Assists', 'Opponent Turnovers', 'Opponent Steals', 'Opponent Blocks', 'Opponent Personal Fouls', 'Opponent Points', 'Opponent Ejections', 'Opponent Foulouts', 'Opponent Rebounds', 'Opponent Two Points Made', 'Opponent Two Points Attempted', 'Opponent Assist Turnover Ratio', 'Games Played', 'Losses Total', 'Wins Total'])

                # Access the required data
                if 'doc' in data:
                    doc = data['doc']
                    for item in doc:
                        if 'teams' in item['data']:
                            teams = item['data']['teams']
                            for team_id, team_data in teams.items():
                                # Collect the data
                                row_data = [
                                    team_id,
                                    team_data['mediumname'],
                                    team_data['name'],
                                    team_data['nickname'],
                                    team_data.get('stats', {}).get('minutes', {}).get('value', ''),
                                    team_data.get('stats', {}).get('field_goals_made', {}).get('value', ''),
                                    team_data.get('stats', {}).get('field_goals_attempted', {}).get('value', ''),
                                    team_data.get('stats', {}).get('field_goals_percentage', {}).get('value', ''),
                                    team_data.get('stats', {}).get('three_points_made', {}).get('value', ''),
                                    team_data.get('stats', {}).get('three_points_attempted', {}).get('value', ''),
                                    team_data.get('stats', {}).get('three_points_percentage', {}).get('value', ''),
                                    team_data.get('stats', {}).get('two_points_made', {}).get('value', ''),
                                    team_data.get('stats', {}).get('two_points_attempted', {}).get('value', ''),
                                    team_data.get('stats', {}).get('blocked_attempts', {}).get('value', ''),
                                    team_data.get('stats', {}).get('free_throws_made', {}).get('value', ''),
                                    team_data.get('stats', {}).get('free_throws_attempted', {}).get('value', ''),
                                    team_data.get('stats', {}).get('free_throws_percentage', {}).get('value', ''),
                                    team_data.get('stats', {}).get('offensive_rebounds', {}).get('value', ''),
                                    team_data.get('stats', {}).get('defensive_rebounds', {}).get('value', ''),
                                    team_data.get('stats', {}).get('rebounds', {}).get('value', ''),
                                    team_data.get('stats', {}).get('turnovers', {}).get('value', ''),
                                    team_data.get('stats', {}).get('steals', {}).get('value', ''),
                                    team_data.get('stats', {}).get('blocks', {}).get('value', ''),
                                    team_data.get('stats', {}).get('assist_turnover_ratio', {}).get('value', ''),
                                    team_data.get('stats', {}).get('personal_fouls', {}).get('value', ''),
                                    team_data.get('stats', {}).get('technical_fouls', {}).get('value', ''),
                                    team_data.get('stats', {}).get('flagrant_fouls', {}).get('value', ''),
                                    team_data.get('stats', {}).get('points', {}).get('value', ''),
                                    team_data.get('stats', {}).get('player_technical_fouls', {}).get('value', ''),
                                    team_data.get('stats', {}).get('team_rebounds', {}).get('value', ''),
                                    team_data.get('stats', {}).get('team_technical_fouls', {}).get('value', ''),
                                    team_data.get('stats', {}).get('team_turnovers', {}).get('value', ''),
                                    team_data.get('stats', {}).get('foulouts', {}).get('value', ''),
                                    team_data.get('stats', {}).get('fast_break_points', {}).get('value', ''),
                                    team_data.get('stats', {}).get('paint_points', {}).get('value', ''),
                                    team_data.get('stats', {}).get('second_chance_points', {}).get('value', ''),
                                    team_data.get('stats', {}).get('points_off_turnovers', {}).get('value', ''),
                                    team_data.get('stats', {}).get('ejections', {}).get('value', ''),
                                    team_data.get('stats', {}).get('turnovers_per_match', {}).get('value', ''),
                                    team_data.get('stats', {}).get('blocks_per_match', {}).get('value', ''),
                                    team_data.get('stats', {}).get('steals_per_match', {}).get('value', ''),
                                    team_data.get('stats', {}).get('opponents_minutes', {}).get('value', ''),
                                    team_data.get('stats', {}).get('opponents_field_goals_made', {}).get('value', ''),
                                    team_data.get('stats', {}).get('opponents_field_goals_attempted', {}).get('value', ''),
                                    team_data.get('stats', {}).get('opponents_three_points_made', {}).get('value', ''),
                                    team_data.get('stats', {}).get('opponents_three_points_attempted', {}).get('value', ''),
                                    team_data.get('stats', {}).get('opponents_free_throws_made', {}).get('value', ''),
                                    team_data.get('stats', {}).get('opponents_free_throws_attempted', {}).get('value', ''),
                                    team_data.get('stats', {}).get('opponents_offensive_rebounds', {}).get('value', ''),
                                    team_data.get('stats', {}).get('opponents_defensive_rebounds', {}).get('value', ''),
                                    team_data.get('stats', {}).get('opponents_assists', {}).get('value', ''),
                                    team_data.get('stats', {}).get('opponents_turnovers', {}).get('value', ''),
                                    team_data.get('stats', {}).get('opponents_steals', {}).get('value', ''),
                                    team_data.get('stats', {}).get('opponents_blocks', {}).get('value', ''),
                                    team_data.get('stats', {}).get('opponents_personal_fouls', {}).get('value', ''),
                                    team_data.get('stats', {}).get('opponents_points', {}).get('value', ''),
                                    team_data.get('stats', {}).get('opponents_ejections', {}).get('value', ''),
                                    team_data.get('stats', {}).get('opponents_foulouts', {}).get('value', ''),
                                    team_data.get('stats', {}).get('opponents_rebounds', {}).get('value', ''),
                                    team_data.get('stats', {}).get('opponent_two_points_made', {}).get('value', ''),
                                    team_data.get('stats', {}).get('opponents_two_points_attempted', {}).get('value', ''),
                                    team_data.get('stats', {}).get('opponents_assist_turnover_ratio', {}).get('value', ''),
                                    team_data.get('stats', {}).get('games_played', {}).get('value', ''),
                                    team_data.get('stats', {}).get('losses_total', {}).get('value', ''),
                                    team_data.get('stats', {}).get('wins_total', {}).get('value', '')
                                ]

                                # Write the row to the CSV file
                                writer.writerow(row_data)

            print("Data has been saved to 'si_scraper_data.csv' file.")

        else:
            print("Failed to fetch data from the website.")
    except Exception as e:
        print("An error occurred:", str(e))

si_scraper()
