import requests

from sportybet import sportybet_create_ticket
from utils import calculate_form_points, calculate_team_points
browser_agent_headers = {'User-Agent':
                             'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
                       }

api_to_model_map = {}

def preprocess(home_team, away_team, df_cleaned, label_encoder, scaler):
    # encode home team
    home_team_encoded = label_encoder.transform([home_team])[0]
    away_team_encoded = label_encoder.transform([away_team])[0]

    # calculate form points
    home_team_recent_form = calculate_form_points(home_team, df_cleaned)
    away_team_recent_form = calculate_form_points(away_team, df_cleaned)

    # average goals per game
    home_team_avg_goals = df_cleaned[df_cleaned['HomeTeam'] == home_team]['FTHG'].mean()
    away_team_avg_goals = df_cleaned[df_cleaned['AwayTeam'] == away_team]['FTAG'].mean()

    # team points
    home_team_points = calculate_team_points(home_team, df_cleaned)
    away_team_points = calculate_team_points(away_team, df_cleaned)

    #combine all features
    features = [home_team_encoded, away_team_encoded, home_team_recent_form, away_team_recent_form, home_team_avg_goals, away_team_avg_goals, home_team_points, away_team_points]

    # scale features
    scaled_features = scaler.transform([features])

    return scaled_features





import pickle
model = pickle.load(open('best_model.pkl', 'rb'))
def predict_game(home: str, away: str):
    processed_input = preprocess(home, away)

    # get model predictions
    home_win_probability, draw_probability, away_win_probability = model.predict(processed_input)
    return home_win_probability, draw_probability, away_win_probability



# Draw no bet type
def generate_sporty_bet_predictions():
    request_data = [
        {
            "sportId": "sr:sport:1",
            "marketId": "1,18,10,29,11,26,36,14",
            "tournamentId": [
                [
                    "sr:tournament:17"
                ]
            ]
        }
    ]
    epl_games_url = "https://www.sportybet.com/api/ng/factsCenter/pcEvents"
    games_object = requests.post(epl_games_url, json=request_data, headers=browser_agent_headers).json()

    if games_object.get('innerMsg') == "Invalid":
        pass

    games = games_object['data'][0]['events'][:10]

    game_parser = []
    for game in games:
        home = game['homeTeamName']
        away = game['awayTeamName']
        home_win_probability, draw_probability, away_win_probability = predict_game(home, away)

        # Market id is constant "11" for Draw no bet
        # Specifier is ""

        # get outcome IDs from event data
        # find draw no bet market
        draw_no_bet_market = list(filter(lambda x: x['id'] == "11", game['markets']))[0]
        home_outcome_id, away_outcome_id = map(lambda x: x['id'], draw_no_bet_market['outcomes'])
        outcome_id = home_outcome_id if home_win_probability > away_win_probability else away_outcome_id

        data = {
            'eventId': game['eventId'],
            "marketId": "11",
            'specifier': "",
            'outcomeId': outcome_id
        }

        game_parser.append(data)
    return game_parser


print(sportybet_create_ticket(generate_sporty_bet_predictions()))