import csv
import requests

def si_nfl_scraper(option, base_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept': 'application/json'
    }

    try:
        response = requests.get(base_url, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON content
            json_results = response.json()

            # Construct the CSV filename based on the option
            csv_filename = f'si_nfl_player_data_{option.replace(" ", "_").lower()}.csv'

            # Open a CSV file in write mode
            with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)

                # Write the header row based on the option
                if option == 'passing':
                    writer.writerow(['Rank', 'Player Name', 'Team', 'Player ID', 'Team ID', 'Season Position', 'Conference', 'Qualified Passing Leader',
                                     'Games Played', 'Passer Rating', 'Passing Completions', 'Passing Attempts', 'Passing Completion pct.', 'Passing Yards',
                                     'Passing Touchdowns', 'Passing Interceptions', 'Passing Yards Per Attempt', 'Passing Yards Per Game', 'Catchable Pass', 'Time Sacked',
                                     'Hurries Allowed', 'Average Pocket Time'])
                elif option == 'rushing':
                    writer.writerow(['Rank', 'Player Name', 'Team', 'Player ID', 'Team ID', 'Season Position', 'Conference',
                                     'Qualified Rushing Leader', 'Games Played', 'Rushing Attempts', 'Rushing Yards', 'Rushing Yards Per Attempts',
                                     'Rushing Touchdowns', 'Rushing Attempts Per Game', 'Rushing Yards Per Game', '1st Downs (Rushing)', 'Rushing Stuff pct.',
                                     'Fumbles', 'Fumbles Lost', 'Rushing Tochdown pct.', 'Rush Yards After Contact Average', 'Rush Yards Before Contact Average', 'Broken Tackles'])
                elif option == 'receiving':
                    writer.writerow(['Rank', 'Player Name', 'Player ID', 'Qualified Receiving Leader', 'Games Played',
                                     'Receiving Targets', 'Receptions', 'Receiving Yards', 'Receiving Touchdowns', 'Targets Per Game',
                                     'Receiving Yards Per Game', 'Yards Per Reception', '1st Down Pct. on Receptions', 'Average Yards at Catch',
                                     'Average Yards After Catch', 'Offensive Receiver Drop', 'Broken Tackles'])
                elif option == 'defense':
                    writer.writerow(['Rank', 'Player Name',  'Player ID', 'Games Played', 'Total Tackles', 'Assists',
                                     'Defensive sacks', 'Defensive Sack Yards', 'Fumbles Forced', 'Passes Defensed', 'Def. Interceptions',
                                     'Def. Inceptions Touchdowns', 'Tackles for Loss', 'Defender Blitz', 'Quarterback Hits', 'Defensive Knockdowns',
                                     'Defensive Hurries', 'Player Individual Pressures', 'Defensive Snaps (player totals)'])
                elif option == 'kicking':
                    writer.writerow(['Rank', 'Player Name', 'Player ID', 'Qualified Field Goals Leader', 'Games Played',
                                     'Kickoff', 'Kickoff Touchbacks', 'Kickoff Touchbacks Pct.', 'Kickoff Yards', 'Average Kickoff Yards',
                                     'Field Goals Made', 'Field Goals Attempted', 'Extra Points Made', 'Extra Points Attempted', 'Extra Point Pct.'])
                elif option == 'punting':
                    writer.writerow(['Rank', 'Player Name', 'Player ID', 'Qualified Punting Leader', 'Games Played',
                                     'Punts', 'Gross Punting Yards', 'Gross Punting Average', 'Punts Blocked', 'Punting Touchbacks',
                                     'Punts Inside 20', 'Punting Long', 'Net Punting Yards', 'Net Punting Average', 'Punt Hang Time'])
                elif option == 'returns':
                    writer.writerow(
                        ['Rank', 'Player Name', 'Team', 'Player ID', 'Team ID', 'Season Position', 'Conference',
                         'Qualified Kickoff Returns Leader', 'Qualified Punt Returns Leader', 'Games Played',
                         'Punt Returns', 'Punt Return Yards', 'Punt Return Average', 'Punt Return Fair Catches',
                         'Punt Return Long', 'Punt Return Touchdowns', 'Kickoff Returns', 'Kickoff Return Yards',
                         'Kickoff Return Average', 'Kickoff Return Long', 'Kickoff Return Touchdowns'])

                # Access the required data
                if 'data' in json_results:
                    for row_data in json_results['data']:
                        # Write the row to the CSV file
                        writer.writerow(row_data)

            print(f"Data for {option} has been saved to '{csv_filename}' file.")

        else:
            print(f"Failed to fetch data from the website for {option}.")
    except Exception as e:
        print(f"An error occurred for {option}: {str(e)}")


# Define a list of options along with their corresponding URLs
options = {
    'passing': 'https://hosted.radar360.sportradar.com/reports/v1/47836070-3c60-11e9-bdac-a5f9825fc570?seasons=2023',
    'rushing': 'https://hosted.radar360.sportradar.com/reports/v1/534c7f40-3c60-11e9-bdac-a5f9825fc570?seasons=2023',
    'receiving': 'https://hosted.radar360.sportradar.com/reports/v1/6235a5b0-c5bb-11e9-9179-f5553d83c3d3?seasons=2023',
    'defense': 'https://hosted.radar360.sportradar.com/reports/v1/0938d0c0-c5bd-11e9-90b4-13b28ac9beb1?seasons=2023',
    'kicking': 'https://hosted.radar360.sportradar.com/reports/v1/78965640-c5bd-11e9-ac90-2dddc9ccba86?seasons=2023',
    'punting': 'https://hosted.radar360.sportradar.com/reports/v1/bbc40f70-c5bd-11e9-b61e-6d16d7ce2c06?seasons=2023',
    'returns': 'https://hosted.radar360.sportradar.com/reports/v1/6d46bc30-3c60-11e9-bdac-a5f9825fc570?seasons=2023'
}

# Iterate through the options and scrape data for each option
for option, base_url in options.items():
    si_nfl_scraper(option, base_url)
