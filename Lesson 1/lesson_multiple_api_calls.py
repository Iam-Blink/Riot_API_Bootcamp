#--------- LOAD LIBRARIES ---------##
from riotwatcher import LolWatcher, RiotWatcher, ApiError #'pip install riotwatcher' 
import pandas as pd
#from dotenv import load_dotenv #'pip install python-dotenv' in Anaconda prompt
#import os


#--------- LOAD CONFIG DATA ---------##
api_key = 'RGAPI-0f38c180-3ae5-4a07-8e83-f4d1eee62619' #it's a 24h expiration key

lol_watcher = LolWatcher(api_key) #Tell LoL Watcher to use LoL functions with the API key
riot_watcher = RiotWatcher(api_key) #Tell Riot Watcher your API key, we need this, to access the account-v1 endpoint


def total_games(player_info):
    total_games = (player_info["wins"] + player_info["losses"])
    return total_games


player_region= 'euw1'.lower() 
player_routing= 'europe'
queue_type = "RANKED_SOLO_5x5"

challenger_ladder = lol_watcher.league.challenger_by_queue(region=player_region,queue=queue_type)

#challenger_ladder is a dictionary, so we have to use a special function to make it into a DataFrame
raw_data = pd.DataFrame.from_dict(challenger_ladder)

raw_data.head(5)


#EXTRACT RELEVANT DATA
#correct way
challenger_players = pd.DataFrame.from_dict(challenger_ladder["entries"])
"""
                                          summonerId  leaguePoints rank  wins  losses  veteran  inactive  freshBlood  hotStreak
0  VbwW0a27h5YU4Orzq9A_Sw58kyyIO-Y_7VU0YtxG0hFGbQ...           584    I    47      17    False     False        True       True
1   TMPDWq_KapjHH2AZtvVFePx3nggAk9AhfXUET0uoX2aia97M           618    I    44      18    False     False        True      False
2    Z2_vgFGFDr5FmnqgDLIGNkn-sFXLzQfAkw4dmIax1RUmSQY           593    I    49      31    False     False        True      False
3  Qb_Mv3HByiyqOvRO6A50P9DvLg4UgRiQ3y1-jnxdwHjzaG...           465    I    40      24    False     False        True      False
4    85cZrzTHoI-sX08QvUcBqNCke8hSfryCBcUQqjigjOKkj7Q           564    I    50      28    False     False        True       True
"""
"""
Incorrect way:
challenger_players = raw_data["entries"]
>>> challenger_players
0    {'summonerId': 'VbwW0a27h5YU4Orzq9A_Sw58kyyIO-...
1    {'summonerId': 'TMPDWq_KapjHH2AZtvVFePx3nggAk9...
2    {'summonerId': 'Z2_vgFGFDr5FmnqgDLIGNkn-sFXLzQ...
4    {'summonerId': '85cZrzTHoI-sX08QvUcBqNCke8hSfr...
"""