import json
import requests
from datetime import datetime as dt
from dateutil import parser
from pprint import pprint

url = "https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds/?apiKey=13fcfd3dd11caea8d5d9f589a6bacf29&regions=us&markets=h2h,spreads,totals&oddsFormat=american"

response = requests.get(url)
raw_data = response.json()
time_stamp = dt.isoformat(dt.today())
with open(f"raw_data_{time_stamp}.json", 'w') as file:
    json.dump(raw_data, file)

start = parser.parse("2023-09-08T00:00:00Z")
stop = parser.parse("2023-09-13T23:59:59Z")

intermediate_data = []
for game in raw_data:
    if start <= parser.parse(game['commence_time']) <= stop:
        team1 = game['away_team']
        team2 = game['home_team']
        for idx, value in enumerate(game['bookmakers']):
            if value['key'] == "draftkings":
                book = idx

        if team1 == game['bookmakers'][book]['markets'][0]['outcomes'][0]['name']:
            team1_line = game['bookmakers'][book]['markets'][0]['outcomes'][0]['price']
            team2_line = game['bookmakers'][book]['markets'][0]['outcomes'][1]['price']
        else:
            team1_line = game['bookmakers'][book]['markets'][0]['outcomes'][1]['price']
            team2_line = game['bookmakers'][book]['markets'][0]['outcomes'][0]['price']

        if team1 == game['bookmakers'][book]['markets'][0]['outcomes'][0]['name']:
            team1_spread = game['bookmakers'][book]['markets'][1]['outcomes'][0]['point']
            team2_spread = game['bookmakers'][book]['markets'][1]['outcomes'][1]['point']
        else:
            team1_spread = game['bookmakers'][book]['markets'][1]['outcomes'][1]['point']
            team2_spread = game['bookmakers'][book]['markets'][1]['outcomes'][0]['point']
        over_under = game['bookmakers'][book]['markets'][2]['outcomes'][0]['point']

        intermediate_data.append({"team1": team1,
                                   "team2": team2,
                                   "team1_line": team1_line,
                                   "team2_line": team2_line,
                                   "team1_spread": team1_spread,
                                   "team2_spread": team2_spread,
                                   "over_under": over_under,
                                })

# with open("sample.json", "w") as outfile:
#     json.dump(dictionary, outfile)

with open('week_1_nfl_odds.json', 'w') as file:
    json.dump(intermediate_data, file)