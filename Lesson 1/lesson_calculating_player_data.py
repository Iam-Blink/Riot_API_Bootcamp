"""
GOALS:
1. Request last 10 games for an account 

/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}
/lol/match/v5/matches/by-puuid/{puuid}/ids

2. Determine the game duration for each match

/lol/match/v5/matches/{matchId}

3. Calculate the average game duration
"""

#--------- LOAD LIBRARIES ---------#
from riotwatcher import LolWatcher, RiotWatcher, ApiError #'pip install riotwatcher' 
import pandas as pd

#--------- LOAD CONFIG DATA ---------#
api_key = 'RGAPI-2aca8186-534f-47cf-a4a0-9a57bc49c04f' #it's a 24h expiration key

lol_watcher = LolWatcher(api_key) #Tell LoL Watcher to use LoL functions with the API key
riot_watcher = RiotWatcher(api_key) #Tell Riot Watcher your API key, we need this, to access the account-v1 endpoint

riot_watcher_player_region= 'europe'.lower() 
lol_watcher_player_region="EUW1".lower() 
player_routing= 'europe'
queue_type = "RANKED_SOLO_5x5"
game_name = "Growing Wings"
tag_line = "EUW"

#--------- Making my own functions  ---------#

def accountPUUID(riot_watcher_player_region, game_name, tag_line):
    account_PUUID = riot_watcher.account.by_riot_id(riot_watcher_player_region,game_name,tag_line)
    return account_PUUID

def last_10_games(lol_watcher_player_region,account_PUUID):
    last10games = lol_watcher.match.matchlist_by_puuid(region=lol_watcher_player_region,puuid=account_PUUID,start=0,count=10)
    return last10games

#--------- Request last 10 games for an account  ---------#

#get PUUID
PUUID = accountPUUID(riot_watcher_player_region, game_name, tag_line)["puuid"]

#get last 10 games
my_last10_games = last_10_games("europe",PUUID)


#--------- Determine the game duration for each match  ---------#
game_durations = []
for game in range(len(my_last10_games)):
    current_match = lol_watcher.match.by_id(lol_watcher_player_region,my_last10_games[game])
    match_duration = current_match["info"]["gameDuration"]
    
    #store in list for next exercise
    game_durations.append([current_match["metadata"]["matchId"],match_duration])
    print("match: ",current_match["metadata"]["matchId"]," duration: ", match_duration)
    
    
#--------- Calculate the average game duration  ---------#

#since its a 2d array, we need to pass only the values of the 2nd column to a new list and sum then together

all_durations = []

for game in range(len(game_durations)):
    #for duration in range(len(game_durations)):
    all_durations.append(game_durations[game][1])

total_durations = sum(all_durations)

print("total durations: ", total_durations)

average_game_duration = total_durations / len(game_durations)

print("average_game_duration:" , average_game_duration)


#could have also done the average() of the list
import statistics as std
std.mean(all_durations)