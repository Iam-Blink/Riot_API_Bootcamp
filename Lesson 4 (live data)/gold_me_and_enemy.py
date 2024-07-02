import requests
import time
import warnings
import sys

##-------- Goals of the lesson --------##

"""
1. Start a live game against a bot
2. Make a request for the live client data
3. Extract your gold and your opponent's gold
4. Determine the difference and plot over time
5. Bonus: check for live events like dragon spawn


To make this we need to use the Live Client Data API from Riot Games (for league of legends) - https://developer.riotgames.com/docs/lol#game-client-api

"""

## before we start, here is an example from a request to the live client data API that gets the current gold of the active player ##

# https://127.0.0.1:2999/liveclientdata/allgamedata

def kbhit():
    if sys.platform.startswith('win'):
        import msvcrt
        return msvcrt.kbhit()
    else:
        import select
        return select.select([sys.stdin], [], [], 0)[0]
    
def get_current_gold():
    url = "https://127.0.0.1:2999/liveclientdata/allgamedata"
    while True:
        warnings.simplefilter("ignore")  # to suppress the warnings about insecure network request
        try:
            response = requests.get(url, verify=False)  # Ignore SSL certificate errors
            data = response.json()
            currentGold = data['activePlayer']['currentGold']
            print(f"{data['activePlayer']['summonerName']} currently has {round(currentGold, 2)}g at {round(data['gameData']['gameTime'], 2)} seconds")
        except requests.exceptions.RequestException as e:
            print("Error making request:", e)
        except KeyError:
            print("Unable to retrieve current gold value from the response.")
        time.sleep(1)  # Wait for 1 second before the next iteration

        # Check for keyboard input
        if kbhit():
            break

# Call the function to run it
get_current_gold()

## bonus: check for live events like dragon spawn, turret destroyed, etc. ##

## function that creates a list of the enemy players in the game ##

def get_enemy_players(data):
    active_player_name = data['activePlayer']['summonerName']
    enemy_players = [player for player in data['allPlayers'] if player['summonerName'] != active_player_name]
    return enemy_players

## Now we will create a function that gets the gold of the enemy players ##

def calculate_player_gold(player, game_time, events):
    # Convert game time to minutes
    total_minutes = game_time / 60

    passive_gold_generation = 2.04 * max(0, total_minutes - 1.50)  # starts at 1:50 min
    gold_from_kills = player['scores']['kills'] * 300  # assuming each kill gives 300 gold
    gold_from_assists = player['scores']['assists'] * 150  # assuming each assist gives 150 gold
    gold_from_creepScore = player['scores']['creepScore'] * 20  # assuming each creepScore gives 20 gold

    # Add gold from events
    gold_from_events = 0
    for event in events["Events"]:
        if event['EventName'] == 'FirstBlood':
            gold_from_events += 100
        elif event['EventName'] == 'TurretKilled':
            gold_from_events += 300
    #this is a simple example, as it doesn't account to who this gold goes to, but it's a start (who is the actor or reviver of the event)

    return passive_gold_generation + gold_from_kills + gold_from_assists + gold_from_creepScore + gold_from_events

def get_enemy_gold():
    url = "https://127.0.0.1:2999/liveclientdata/allgamedata"
    while True:
        warnings.simplefilter("ignore")  # to suppress the warnings about insecure network request
        try:
            response = requests.get(url, verify=False)  # Ignore SSL certificate errors
            data = response.json()
            active_player = data['activePlayer']
            enemy_players = get_enemy_players(data)
            enemy_gold = []
            for player in enemy_players:
                if player['summonerName'] != active_player['summonerName']:
                    game_time = data['gameData']['gameTime']
                    events = data['events']  # Get the events data
                    enemy_gold = [round(calculate_player_gold(player, game_time, events), 2) for player in enemy_players]
            print(f"Enemy gold: {enemy_gold} at {round(data['gameData']['gameTime'], 2)} seconds")
        except requests.exceptions.RequestException as e:
            print("Error making request:", e)
        except KeyError:
            print("Unable to retrieve enemy gold value from the response.")
        time.sleep(1)  # Wait for 1 second before the next iteration

        # Check for keyboard input
        if kbhit():
            break
       
       
# Call the function to run it
get_enemy_gold()

"""
I had a problem before, we have to check the data structure of the response to see if the data we are trying to access is there. The currentGold key is not present in the allPlayers array, so we need to find the correct key to access the gold of the enemy players.
Seems like the problem lies in the fact that the data structure is not as expected

In the allPlayers array, the individual items (players) don't have a key "currentGold". Their data structure is as follows:

{
			"championName": "Shyvana",
			"isBot": true,
			"isDead": false,
			"items": [
				{
					"canUse": false,
					"consumable": false,
					"count": 1,
					"displayName": "Doran's Ring",
					"itemID": 1056,
					"price": 400,
					"rawDescription": "GeneratedTip_Item_1056_Description",
					"rawDisplayName": "Item_1056_Name",
					"slot": 0
				},
				{
					"canUse": true,
					"consumable": true,
					"count": 2,
					"displayName": "Health Potion",
					"itemID": 2003,
					"price": 50,
					"rawDescription": "GeneratedTip_Item_2003_Description",
					"rawDisplayName": "Item_2003_Name",
					"slot": 1
				},
				{
					"canUse": true,
					"consumable": false,
					"count": 1,
					"displayName": "Stealth Ward",
					"itemID": 3340,
					"price": 0,
					"rawDescription": "GeneratedTip_Item_3340_Description",
					"rawDisplayName": "Item_3340_Name",
					"slot": 6
				}
			],
			"level": 4,
			"position": "JUNGLE",
			"rawChampionName": "game_character_displayname_Shyvana",
			"respawnTimer": 0.0,
			"riotId": "Shyvana#BOT",
			"riotIdGameName": "Shyvana",
			"riotIdTagLine": "BOT",
			"runes": {
				"keystone": {
					"displayName": "Grasp of the Undying",
					"id": 8437,
					"rawDescription": "perk_tooltip_GraspOfTheUndying",
					"rawDisplayName": "perk_displayname_GraspOfTheUndying"
				},
				"primaryRuneTree": {
					"displayName": "Resolve",
					"id": 8400,
					"rawDescription": "perkstyle_tooltip_7204",
					"rawDisplayName": "perkstyle_displayname_7204"
				},
				"secondaryRuneTree": {
					"displayName": "Sorcery",
					"id": 8200,
					"rawDescription": "perkstyle_tooltip_7202",
					"rawDisplayName": "perkstyle_displayname_7202"
				}
			},
			"scores": {
				"assists": 0,
				"creepScore": 10,
				"deaths": 0,
				"kills": 0,
				"wardScore": 0.0
			},
			"skinID": 0,
			"summonerName": "Shyvana Bot",
			"summonerSpells": {
				"summonerSpellOne": {
					"displayName": "Ghost",
					"rawDescription": "GeneratedTip_SummonerSpell_SummonerHaste_Description",
					"rawDisplayName": "GeneratedTip_SummonerSpell_SummonerHaste_DisplayName"
				},
				"summonerSpellTwo": {
					"displayName": "Heal",
					"rawDescription": "GeneratedTip_SummonerSpell_SummonerHeal_Description",
					"rawDisplayName": "GeneratedTip_SummonerSpell_SummonerHeal_DisplayName"
				}
			},
			"team": "CHAOS"
}
"""
"""
Gonna debug here, the code is not working as expected
"""
"""
json_game_file = "some data\game_data.json"

with open(json_game_file, 'r') as file:
    game_data = json.load(file)


game_data.keys()

active_player_t = game_data['activePlayer']["summonerName"]
all_players_t = game_data['allPlayers']

def get_enemy_players(data):
    active_player_name = data['activePlayer']['summonerName']
    enemy_players = [player for player in data['allPlayers'] if player['summonerName'] != active_player_name]
    return enemy_players

get_enemy_players(game_data)
"""
"""
Debuggin finishes here
"""


## Now we will create a function that plots the gold difference over time ##

import matplotlib.pyplot as plt

def plot_gold_difference():
    url = "https://127.0.0.1:2999/liveclientdata/allgamedata"
    gold_difference = []

    while True:
        warnings.simplefilter("ignore")  # to suppress the warnings about insecure network request
        try:
            response = requests.get(url, verify=False)  # Ignore SSL certificate errors
            data = response.json()

            # Get the gold for the active player and the enemy players
            active_player_gold = data['activePlayer']['currentGold']
            enemy_players = get_enemy_players(data)
            game_time = data['gameData']['gameTime']
            enemy_gold = [round(calculate_player_gold(player, game_time),2) for player in enemy_players]

            # Calculate the gold difference
            gold_difference.append(active_player_gold - sum(enemy_gold))

            # Plot the gold difference
            plt.plot(gold_difference)
            plt.ylabel('Gold Difference')
            plt.draw()
            plt.pause(1)  # pause for 1 second

            # Clear the plot for the next plot
            plt.clf()

        except requests.exceptions.RequestException as e:
            print(e)
            time.sleep(5)  # wait for 5 seconds before trying again

plot_gold_difference()


## export the game data to a JSON file ##
import json

def export_game_data():
    url = "https://127.0.0.1:2999/liveclientdata/allgamedata"
    while True:
        warnings.simplefilter("ignore")  # to suppress the warnings about insecure network request
        try:
            response = requests.get(url, verify=False)  # Ignore SSL certificate errors
            data = response.json()
            with open('game_data.json', 'w') as file:
                json.dump(data, file)
            print("Game data exported successfully.")
        except requests.exceptions.RequestException as e:
            print("Error making request:", e)
        time.sleep(1)  # Wait for 1 second before the next iteration

        # Check for keyboard input
        if kbhit():
            break

# Call the function to run it
export_game_data()

