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
            csv_filename = f'si_scraper_data_{option.replace(" ", "_").lower()}.csv'

            # Open a CSV file in write mode
            with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)

                # Write the header row based on the option
                if option == 'Offense':
                    writer.writerow(['Rank', 'Team Name', 'Team ID', 'Conference', 'Games Played', 'Points', 'Field Goals Made', 'Field Goals Attempted', 'Field Goals Percentage', 'Total Yards', 'Pass Yards', 'Rush Yards', 'Penalties', 'Penalty Yards', 'Turnovers', 'Fumbles Lost', 'Interceptions Thrown'])
                elif option == 'Offense-Advanced':
                    writer.writerow(['Rank', 'Team Name', 'Team ID', 'Conferenece', 'Games Played', 'Red Zone Drives - Touchdown Pct.', 'Red Zone Drives - Scoring Pct.', 'Red Zone Drives (Total)', 'Two Point Conversion Pct. ', 'Passing Pct.', 'Rushing Pct.', 'Turnover Differential', 'Big Plays Per Game'])
                elif option == 'Defence I':
                    writer.writerow(['Rank', 'Team Name', 'Team ID', 'Conference', 'Games Played', 'Points Allowed (play by play)', 'Points Allowed per Game (play by play)', 'Total Yards (Net) Allowed', 'Total Yards (Net) Allowed per Game', 'Defensive Net Passing Yards', 'Defensive Net Passing Yards Per Game', 'Rushing Yards Allowed', 'Defensive Rushing Yards Per Game'  ])
                elif option == 'Defence II':
                    writer.writerow(['Rank', 'Team Name', 'Team ID', 'Conference', 'Games Played', 'Defensive sack Yards', 'Fumbles Forced', 'Passes Defensed', 'Def. Interceptions', 'Def. Interception Yards', 'Def. Interception Touchdowns', 'Safeties', 'Total Tackles', 'Tackles for loss', 'Quarterback Hits'])
                elif option == 'Defence-Advanced':
                    writer.writerow(['Rank', 'Team Name', 'Team ID', 'Conference', 'Games Played', 'Defensive Missed Tackles', 'Defensive Missed Tackle Pct.', 'Defensive Hurries', 'Defensive Knockdowns', 'Defensive Blitz Pct.', 'Defensive 3rd Down Pct.'])

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
    'Offense': 'https://hosted.radar360.sportradar.com/reports/v1/55d198f0-3c5f-11e9-b44b-85da4e005e34?seasons=2023',
    'Offense-Advanced': 'https://hosted.radar360.sportradar.com/reports/v1/e69e1430-3c5f-11e9-bdac-a5f9825fc570?seasons=2023',
    'Defence I': 'https://hosted.radar360.sportradar.com/reports/v1/31899d20-3c60-11e9-bdac-a5f9825fc570?seasons=2023',
    'Defence II': 'https://hosted.radar360.sportradar.com/reports/v1/33f91680-3c60-11e9-bdac-a5f9825fc570?seasons=2023',
    'Defence-Advanced': 'https://hosted.radar360.sportradar.com/reports/v1/414cf400-3c60-11e9-bdac-a5f9825fc570?seasons=2023'
}

# Iterate through the options and scrape data for each option
for option, base_url in options.items():
    si_nfl_scraper(option, base_url)
