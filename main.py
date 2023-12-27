# football api
from espn_api.football import League
league = League(league_id=1245, year=2018)
print(league.teams)
