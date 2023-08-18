import json
from pprint import pprint

games = []

if __name__ == '__main__':
    week = input("What week? ")
    while True:
        team1 = input("Team 1: ")
        if team1.lower() == "q" or team1.lower() == "quit":
            break
        team1_line = float(input("Team 1 Line: "))
        team1_spread = float(input("Team 1 Spread: "))
        team2 = input("Team 2: ")
        team2_line = float(input("Team 2 Line: "))
        team2_spread = -team1_spread
        print(f"Team 2 Spread: {team2_spread}")
        over_under = float(input("Over/Under: "))
        games.append({"team1": team1,
                    "team2": team2,
                    "team1_line": team1_line,
                    "team2_line": team2_line,
                    "team1_spread": team1_spread,
                    "team2_spread": team2_spread,
                    "over_under": over_under,
        })

    json_object = json.dumps(games, indent=4)
    
    # Writing to sample.json
    with open(f"week_{week}_games.json", "w") as outfile:
        outfile.write(json_object)