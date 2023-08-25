import json
# from games import games

print()
week = input("What week? ")

with open(f'week_{week}_nfl_odds.json', 'r') as openfile:
 
    # Reading from json file
    games = json.load(openfile)

VIG = -110

wager = float(input("Enter bet (default=100): ") or 100)

def underdog(line, bet=wager):
    return bet + (bet * line/100)

def favorite(line, bet=wager):
    return bet + (abs(bet / (line/100)))

def spread(bet):
    return bet + (abs(bet / (VIG/100)))

def display_game(game):
    result = ""
    result += f"{game['team1']} v. {game['team2']}\n"
    result += f"Bet = ${wager:.2f}\n"
    result += f"Over/Under: {game['over_under']}\n"
    if game['team1_spread'] > 0:
        result += f"Spread: {game['team1']} +{game['team1_spread']} points.\n"
    else:
        result += f"Spread: {game['team2']} +{game['team2_spread']} points.\n"
    result += "Money Line:\n"
    if game['team1_line'] > 0:
        result += f"\t{game['team1']}: {game['team1_line']} -> ${underdog(game['team1_line']):.2f}\n"
        result += f"\t{game['team2']}: {game['team2_line']} -> ${favorite(game['team2_line']):.2f}\n"
    else:
        result += f"\t{game['team1']}: {game['team1_line']} -> ${favorite(game['team1_line']):.2f}\n"
        result += f"\t{game['team2']}: {game['team2_line']} -> ${underdog(game['team2_line']):.2f}\n" 
    result += f"Spread, Over/Under Payout -> ${spread(wager):.2f}\n\n"
    return result

print()
results = ""
for game in games:
    result = display_game(game)
    results += result
    

longest_shot = [games[0]]
for game in games:
    if abs(game['team1_line'] - game['team2_line']) > abs(longest_shot[0]['team1_line'] - longest_shot[0]['team2_line']):
        longest_shot[0] = game

biggest_spread = [games[0]]
for game in games:
    if abs(game['team1_spread']) > abs(biggest_spread[0]['team1_spread']):
        biggest_spread[0] = game

smallest_spread = [games[0]]
for game in games:
    if abs(game['team1_spread']) < abs(smallest_spread[0]['team1_spread']):
        smallest_spread[0] = game

print(f"Week {week}\n")
print()
print("Longest Shot / Surest Thing:")
print(display_game(longest_shot[0]).rstrip())
print()
print("Biggest Spread:")
print(display_game(biggest_spread[0]).rstrip())
print()
print("Smallest Spread:")
print(display_game(smallest_spread[0]).rstrip())
print()
print("Game Odds:")
print(results)

consolidated = f""" 
Week {week}

Longest Shot / Surest Thing:
{display_game(longest_shot[0]).rstrip()}

Biggest Spread: 
{display_game(biggest_spread[0]).rstrip()}

Smallest Spread:
{display_game(smallest_spread[0]).rstrip()}


Game Odds:
{results}
"""

# with open(f"week_{week}_lines.txt", mode='w') as file:
#     file.write(consolidated)
