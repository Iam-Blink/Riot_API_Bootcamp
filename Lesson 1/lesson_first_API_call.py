"""
Important note, the endpoint https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name no longer works, it gives 400

Because riot no longer uses SummonerNames, i think they deprecated this endpoint. So we have to use the https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name/tagline} endpoint

"""

#--------- LOAD LIBRARIES ---------##
from riotwatcher import LolWatcher, RiotWatcher, ApiError #'pip install riotwatcher' 
#from dotenv import load_dotenv #'pip install python-dotenv' in Anaconda prompt
#import os


#--------- LOAD CONFIG DATA ---------##
api_key = 'RGAPI-2aca8186-534f-47cf-a4a0-9a57bc49c04f' #it's a 24h expiration key

lol_watcher = LolWatcher(api_key) #Tell LoL Watcher to use LoL functions with the API key
riot_watcher = RiotWatcher(api_key) #Tell Riot Watcher your API key, we need this, to access the account-v1 endpoint

#--------- SET PLAYER PARAMETERS ---------##
player_name= 'Growing Wings'.lower()
player_tag="EUW" #adding tag, because now its needed for Riot ID
player_region= 'europe'.lower() #[BR1, EUN1, EUW1, JP1, KR, LA1, LA2, NA1, OC1, TR1, RU]  
player_routing= 'europe'
#api_endpoint = riotwatcher.AccountApi


#--------- CREATE PLAYER OBJECT ---------##
# This is equivalent to going to /riot/account/v1/accounts/by-riot-id/
summoner = riot_watcher.account.by_riot_id(player_region, player_name,player_tag)


# "old call for the summonerv4 endoint by name, now we use account-v1
#summoner= lol_watcher.summoner.by_name(player_region, player_name)
"""
400 Client Error: Bad Request for url: https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/growing%20wings

deprecated endpoint? (https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/)
"""
#summoner= lol_watcher.summoner.by_name(region= 'NA1', summoner_name= 'RebirthNA')
print('Player info= \n',summoner)


#--------- Get a list of past matches ---------##
matchlist= lol_watcher.match.matchlist_by_puuid(region= player_region, puuid= summoner['puuid'])
print('Recent matchID=\n', matchlist)