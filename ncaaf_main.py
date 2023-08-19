import json

# from games import games



with open('./ncaaf_games.json', 'r') as openfile:
 
    # Reading from json file
    games = json.load(openfile)

VIG = -110

wager = 0



def underdog(line, bet=wager):
    return f"{bet + (bet * line/100):.2f}"

def favorite(line, bet=wager):
    return f"{bet + (abs(bet / (line/100))):.2f}"

def spread(bet):
    return f"{bet + (abs(bet / (VIG/100))):.2f}"

def display_game(game, bet):
    result = ""
    result += f"{game['team1']} v. {game['team2']}\n"
    result += f"Bet = ${wager:.2f}\n"
    result += f"Over/Under: {game['over_under']}\n"
    if game['team1_spread'] < 0:
        result += f"Spread: {game['team1']}  {game['team1_spread']} points.\n"
    else:
        result += f"Spread: {game['team2']}  {game['team2_spread']} points.\n"
    result += "Money Line:\n"
    if game['team1_line'] > 0:
        result += f"\t{game['team1']}: {game['team1_line']} -> ${underdog(game['team1_line'], bet)}\n"
        result += f"\t{game['team2']}: {game['team2_line']} -> ${favorite(game['team2_line'], bet)}\n"
    else:
        result += f"\t{game['team1']}: {game['team1_line']} -> ${favorite(game['team1_line'], bet)}\n"
        result += f"\t{game['team2']}: {game['team2_line']} -> ${underdog(game['team2_line'], bet)}\n" 
    result += f"Spread, Over/Under Payout -> ${spread(bet)}\n\n"
    return result


def display_game_html(game, bet):
    result = "<pre style='font-size: 1rem; font-family: Arial, Helvetica, sans-serif;'><br>"
    if game['team1_spread'] < 0:
        result += f"<b>{game['team1']}</b> v. {game['team2']}<br>"
    else:
        result += f"{game['team1']} v. <b>{game['team2']}</b><br>"
    result += f"Bet = ${wager:.2f}<br>"
    result += f"Over/Under: {game['over_under']}<br>"
    if game['team1_spread'] < 0:
        result += f"Spread: <b>{game['team1']}</b> {game['team1_spread']} points.<br>"
    else:
        result += f"Spread: <b>{game['team2']}</b> {game['team2_spread']} points.<br>"
    result += "Money Line:<br>"
    if game['team1_line'] > 0:
        result += f"\t{game['team1']}: {game['team1_line']} -> ${underdog(game['team1_line'], bet)}<br>"
        result += f"\t{game['team2']}: {game['team2_line']} -> ${favorite(game['team2_line'], bet)}<br>"
    else:
        result += f"\t{game['team1']}: {game['team1_line']} -> ${favorite(game['team1_line'], bet)}<br>"
        result += f"\t{game['team2']}: {game['team2_line']} -> ${underdog(game['team2_line'], bet)}<br>" 
    result += f"Spread, Over/Under Payout -> ${spread(bet)}<br><br>"
    result += "</pre>"
    return result


    
    
def go():
    global games
    global wager
    wager = float(Element('bet').value)
    longest_shot = [games[0]]
    for game in games:
        if abs(game['team1_line'] - game['team2_line']) > abs(longest_shot[0]['team1_line'] - longest_shot[0]['team2_line']):
            longest_shot[0] = game
        display = display_game_html(longest_shot[0], wager)
        outputdiv = Element('longestshot')
        outputdiv.element.innerHTML = "<h4 class='text-center'>Longest Shot</h4>" + display

    biggest_spread = [games[0]]
    for game in games:
        if abs(game['team1_spread']) > abs(biggest_spread[0]['team1_spread']):
            biggest_spread[0] = game
        display = display_game_html(biggest_spread[0], wager)
        outputdiv = Element('biggestspread')
        outputdiv.element.innerHTML = "<h4 class='text-center'>Biggest Spread</h4>" + display

    smallest_spread = [games[0]]
    for game in games:
        if abs(game['team1_spread']) < abs(smallest_spread[0]['team1_spread']):
            smallest_spread[0] = game
        display = display_game_html(smallest_spread[0], wager)
        outputdiv = Element('smallestspread')
        outputdiv.element.innerHTML = "<h4 class='text-center'>Smallest Spread</h4>" + display

    all_odds1 = ""
    all_odds2 = ""
    line = len(games) // 2
    for game in games[:line]:
        all_odds1 += display_game_html(game, wager)
    outputdiv = Element('all_odds1')
    outputdiv.element.innerHTML = all_odds1       
    for game in games[line:]:
        all_odds2 += display_game_html(game, wager)
    outputdiv2 = Element('all_odds2')
    outputdiv2.element.innerHTML = all_odds2   

    outputdiv3 = Element('all_odds_header')
    outputdiv3.element.innerHTML = "<h4 class='text-center'>All Odds</h4>"   

