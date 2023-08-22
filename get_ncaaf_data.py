# -Set 'start' and 'stop' in isoformat
# -Change week number in file creation at bottom of code
# -You can change 'book' at or around line 28
# -Copy contents of file created by this script to 'ncaaf_games.json'
# -Change week at top of 'ncaaf.html' and push repo to GitHub

import json
import requests
from datetime import datetime as dt
from dateutil import parser
from pprint import pprint

url = "https://api.the-odds-api.com/v4/sports/americanfootball_ncaaf/odds/?apiKey=13fcfd3dd11caea8d5d9f589a6bacf29&regions=us&markets=h2h,spreads,totals&oddsFormat=american"

response = requests.get(url)
raw_data = response.json()
time_stamp = dt.isoformat(dt.today())
with open(f"ncaaf_raw_data_{time_stamp}.json", 'w') as file:
    json.dump(raw_data, file)

start = parser.parse("2023-08-26T00:00:00Z")
stop = parser.parse("2023-09-05T23:59:59Z")

intermediate_data = []
for game in raw_data:
    if start <= parser.parse(game['commence_time']) <= stop:
        team1 = game['away_team']
        team2 = game['home_team']
        for idx, value in enumerate(game['bookmakers']):
            if value['key'] == "draftkings":
                book = idx

        if game['bookmakers'][book]['markets'][0]['key'] == "h2h" and \
            game['bookmakers'][book]['markets'][1]['key'] == "spreads":

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
            try:
                over_under = game['bookmakers'][book]['markets'][2]['outcomes'][0]['point']
            except IndexError:
                over_under = "N/A"

        elif game['bookmakers'][book]['markets'][0]['key'] == "spreads" and \
            game['bookmakers'][book]['markets'][1]['key'] == "totals":

            team1_line = "N/A"
            team2_line = "N/A"

            if team1 == game['bookmakers'][book]['markets'][0]['outcomes'][0]['name']:
                team1_spread = game['bookmakers'][book]['markets'][0]['outcomes'][0]['point']
                team2_spread = game['bookmakers'][book]['markets'][0]['outcomes'][1]['point']
            else:
                team1_spread = game['bookmakers'][book]['markets'][0]['outcomes'][1]['point']
                team2_spread = game['bookmakers'][book]['markets'][0]['outcomes'][0]['point']
            try:
                over_under = game['bookmakers'][book]['markets'][1]['outcomes'][0]['point']
            except IndexError:
                over_under = "N/A"


        game_time_iso = parser.parse(game['commence_time'])
        game_time = game_time_iso.astimezone().ctime()

        intermediate_data.append({"team1": team1,
                                   "team2": team2,
                                   "team1_line": team1_line,
                                   "team2_line": team2_line,
                                   "team1_spread": team1_spread,
                                   "team2_spread": team2_spread,
                                   "over_under": over_under,
                                   "game_time": game_time
                                })

# with open("sample.json", "w") as outfile:
#     json.dump(dictionary, outfile)

with open('week_1_ncaaf_odds.json', 'w') as file:
    json.dump(intermediate_data, file)