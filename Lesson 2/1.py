"""
Objectives:
1. Get list of challenger players

2. Get last 10 matches for each player
Bonus: Check for duplicates of matchID to ensure not making multiple requests [see file attached as an example]

3. Request match data from list of matchIDs

4. Determine role for each player from match data

5. Store the main role for each player based on past 10 matches

6. Compare to even 20% distribution for each role
Bonus: What does this tell you about role agency? How about player preferences?
"""

#--------- LOAD LIBRARIES ---------#
from riotwatcher import LolWatcher, RiotWatcher, ApiError #'pip install riotwatcher' 
import pandas as pd

#--------- LOAD CONFIG DATA ---------#
api_key = 'RGAPI-48f7ef28-095e-4927-8d39-0dc90f74297d' #it's a 24h expiration key

lol_watcher = LolWatcher(api_key) #Tell LoL Watcher to use LoL functions with the API key
riot_watcher = RiotWatcher(api_key) #Tell Riot Watcher your API key, we need this, to access the account-v1 endpoint

riot_watcher_player_region= 'europe'.lower() 
lol_watcher_player_region="EUW1".lower()
player_routing= 'europe'
queue_type = "RANKED_SOLO_5x5"
game_name = "Growing Wings"
tag_line = "EUW"

#--------- 1. Get list of challenger players ---------#

challenger_queue = lol_watcher.league.challenger_by_queue(lol_watcher_player_region,queue_type)

challenger_df = pd.DataFrame.from_dict(challenger_queue["entries"]).sort_values(["leaguePoints"],ascending=False)

#--------- 2. Get last 10 matches for each player ---------#
#Bonus: Check for duplicates of matchID to ensure not making multiple requests [see file attached as an example] ---------#

challengers = challenger_df["summonerId"].to_list() #by summonerId

#get PUUIDs by summonerId
summoners = []

for challenger in range(len(challengers)):
    summoners.append(lol_watcher.summoner.by_id(lol_watcher_player_region,challengers[challenger])["puuid"])

#get matches

matches = []
player_and_match = []

for ppuid in range(len(summoners)):
    matches.append(lol_watcher.match.matchlist_by_puuid(lol_watcher_player_region,summoners[ppuid],count=10))
    player_and_match.append([summoners[ppuid],matches[ppuid]])
    
print(player_and_match)

test = pd.DataFrame.from_records(player_and_match, columns=["Player","MatchIDs"])

#here check for duplicates first, by creating a dict (which removes the duplicated keys automatically, since keys cant be duplicate), so no summoner can be duplicated
#later I create a pandas df checking for duplicated rows, which ensures no match is duplicated

#player_and_match_dict = dict.fromkeys(player_and_match[0][1],player_and_match[0][0])

dict_player_matches = dict(zip(summoners, matches))

new_challenger_matches = pd.DataFrame.from_dict(dict_player_matches)

print(new_challenger_matches.duplicated(keep=False))

new_challenger_matches.head()

#--------- 3. Request match data from list of matchIDs ---------#

match_history = []
""" old version, not working
for player in range(len(summoners)):
    for match in range(len(matches)):
        match_history.append([summoners[player] , [lol_watcher.match.by_id(lol_watcher_player_region,matches[player][match])["info"]["participants"]]])
        
len(match_history)
"""

for player, matches in player_and_match:
  for match_id in matches:  # Iterate through match IDs (strings)
    participant_data = lol_watcher.match.by_id(lol_watcher_player_region, match_id)["info"]["participants"]
    match_history.append([player, participant_data])
    
len(match_history)
#export to file (1 match)

import json

match_exported = json.dumps(match_history[0][1][1])

print(match_exported)

with open("match_1.json", "w") as outfile:
    outfile.write(match_exported)
    

#export to file (all match data - for future use)

match_history_data = match_history

match_history_data = json.dumps(match_history_data)

with open("player_and_10_games_match_data.json", "w") as outfile:
    outfile.write(match_history_data)

#--------- 4. Determine role for each player from match data ---------#

#each match, from each challenger, has 10 participants. We must get the role only of the challenger (we don't care about the rest)

challenger_player_position = []

    
test_player = match_history[0][0]
test_match = match_history[0][1]
participant = match_history[0][1][0]

participant["puuid"]
"""
for player_t, match_t in match_history:
    match_info = match_t[0]
    if match_info["puuid"] == player_t:
        challenger_player_position.append([match_info["puuid"], match_info["individualPosition"]])
"""
for player_t, match_t in match_history:
  # Assuming you don't need a copy (remove unnecessary slicing)
  match_info = match_t[0]  # Access the first element directly
  if "puuid" in match_info and isinstance(match_info, dict):  # Check for key and type
    if match_info["puuid"] == player_t:
      challenger_player_position.append([match_info["puuid"], match_info["individualPosition"]])
  else:
    # Handle cases where match data is missing or not a dictionary (optional)
    print(f"Match data for {player_t} might be missing or invalid")

len(challenger_player_position)

#--------- 5. Store the main role for each player based on past 10 matches ---------#

challenger_player_position_df = pd.DataFrame.from_records(challenger_player_position, columns=["PUUID", "Position"])

last_df = challenger_player_position_df.drop_duplicates(subset=["PUUID"])

"""
Last change, would be to modify and make a condition (when "individualPosition" is "Invalid", use "lane")
"""


"""
                                                PUUID Position
0   QJ7eqBG6a3SADffTf0oWVbysFgpqxOId4rfKN5GerQUzo1...      TOP
1   vzH3LdFZfm3DJ_FCZQvnGf1LElZPX7jAmBNm5HRZCpf6RO...      TOP
2   A2rpLJAwv2DXTi982zbrMmT5EcXGV43Sflw7D2G3dfO2Md...      TOP
4   bJSokMjTYDT8sGBX3tL2r6bQHV6vC8u6DCPJGBNOY4sXuc...      TOP
5   bnGHvPJyE4xPU5_MhYDCfedTS-z9pFp5uYhOm3nkYjmPy8...      TOP
10  iJWAwXvU90eWrTxamWeNbYmy-OFD9nzcCUsKPlVn33rdb1...      TOP
11  vJpmQ1eR4F9EVqDns1gljIa37yde1muYaAxsdJvhrevk-2...      TOP
12  d1OYoTHSzo-VNsDuZZjehJ_gw4HS19pjuMmgwBqCWFNBZC...      TOP
17  FyCg3TbJfUaQ2Xyhm32hK_CDPGEJ_K2VIo7A83JTq59MpA...      TOP
18  qsZ0sEh7XtlxhNbYdSDhVNa1JkOAKtOopoOBHEnMUHoaGJ...      TOP
19  MqW-0wctOmvSoxbyjhyDtXf5WoZRvc61GAU4shk4QOB3tj...   BOTTOM
20  DaS9awsLGKWbHPhTnA1HIXI9bL1ODcMwINMVe5R_v3XXgj...  Invalid
22  Y22ei79vhLD0qzB7pW0J3h-3RfEYN_YxZXgvsJdYFvPyzh...      TOP
24  zYRgNyrk5Y1RhGGZ58LtA4VAR-ibHlZVmDn-kWUfWKcrLx...   BOTTOM
25  HQtGO1hyZhLyA2kdCy_S3GeKATi6NzGYDh66gC4LeQfzth...      TOP
32  CBX-RJvfwXmzQ8wJyQDBpNO4A10gxK3vj1YTkP40TlxGpG...   BOTTOM
33  jx4kZ_9GRwfnvhk3j0hhokmwQIhxYyqTDi_6Ufjvd3Apj2...      TOP
47  wky-yGUXqtDZb__CHraUqIsENF0ZNDftWm7YYzTMn45prs...      TOP
49  DNZ5wjHdJqz4ZPua_ALX4-ZEkMwwSKBrLJzolgNkvH27bv...  Invalid
51  W3iXv4-0-j8nXQdw9s66ZC-0-vRa73D3lxdb4mayCvDkBd...      TOP
54  wyZCQI0-tDimmgmF_vSHZAamvdIRDHj_bGU5-dl3aGHKb4...  Invalid
55  0JobmCro6cIQu89334Mip3Z9sNqncXxS2lkFKRUSgeY89-...      TOP
61  DPVmZJvMLiAu1I_ku8JuYcHfdW0fObTfO1NbM8w_nHh5sv...      TOP
62  yKQ7hQF8VIB-OiPXVeABCloqxDY4412Ozm4-wb4pv7QnEZ...  Invalid
64  nkaLOXK9qM6Xrit1Tbc4t7L98J06VnOUm6VmQSicHBJVAy...   JUNGLE
67  m5O_SzSzbW4I8DRDz4S_yoPI3xBHFx6mxk0Sf7fA7ogDI9...      TOP
68  xsPqnytWaxPIu6akguRkCWopOaCLpRTdayEq1N5HAqWLWy...  Invalid
69  WJxIsUjKq_EOuotvis9O9pB84iNPIIxI60WNpSLn6AwUGG...      TOP
74  K3TlpMf6RBiO5dgo1wYfy-q8blI3Ul1BE8fYFbPh4J3u4q...      TOP
77  tDgQo6b7PNXcIKq5H_QfCV-omInqLX9hXpI8fqo8i7mQSD...      TOP
"""