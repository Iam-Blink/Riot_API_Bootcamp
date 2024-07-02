"""
-Practice working with static data by diving into the relationships between item components and completed items
--Instructions

---Systematically determine which items are shared by class “mythics”
    Lost chapter for mages
    Noonquiver for ADCs
    Serrated Dirk (or brutalizer) for AD assassins
    Hextech Alternator for AP assassins
    Bami’s Cinder for tanks

---Determine the amount of cs required to get the gold for the item
    See average gold/wave (https://leagueoflegends.fandom.com/wiki/Minion_(League_of_Legends)#Wave_Gold_Value)
    
---What game time does this occur at?
        See timing and behavior (https://leagueoflegends.fandom.com/wiki/Minion_(League_of_Legends)#Minion_waves)
        
---Bonus: what if you include tower plates? 125g local gold for each
"""

import pandas as pd
from riotwatcher import riotwatcher, LolWatcher
import json
import jmespath #needed for searching in the json
import os

#Systematically determine which items are shared by class “mythics”

#I can't complete this objective, because we no longer have mythics (I tried checking previous patches and still don't see them)

#I will change this task to:

#-- 1. Determine which items are for which class  --#

"""
This can be done by:
    -Identifying which stats exist (✅)
    -Decide (based on my knowledge) which stats are used for which roles (tank: HP, armor, ...) (✅)
    -Find out what stats each item has (✅)
    -Give a categorization of what role this item belongs to ( )
    -Some mixture could happen ( )
"""

with open("G:\\My Drive\\2024\LoL AI Project (BlinkAI)\\Bootcamp Riot API\\Lesson 3\\item.json") as file:
    full_item_data = json.load(file)
    #print(full_item_data)

stats = dict(full_item_data["basic"]["stats"])

stats.keys()

#we need to drop all that start with "r", because those are stats that come from runes

list_stats = list(stats.keys())

for item in list_stats[:]:
    if item.startswith("r"):
        list_stats.remove(item)
        
print(list_stats)

#Decide (based on my knowledge) which stats are used for which roles

"""
['FlatHPPoolMod', 'FlatMPPoolMod', 'PercentHPPoolMod', 'PercentMPPoolMod', 'FlatHPRegenMod', 'PercentHPRegenMod', 'FlatMPRegenMod', 'PercentMPRegenMod', 'FlatArmorMod', 
'PercentArmorMod', 'FlatPhysicalDamageMod', 'PercentPhysicalDamageMod', 'FlatMagicDamageMod', 'PercentMagicDamageMod', 'FlatMovementSpeedMod', 'PercentMovementSpeedMod', 
'FlatAttackSpeedMod', 'PercentAttackSpeedMod', 'PercentDodgeMod', 'FlatCritChanceMod', 'PercentCritChanceMod', 'FlatCritDamageMod', 'PercentCritDamageMod', 'FlatBlockMod',
'PercentBlockMod', 'FlatSpellBlockMod', 'PercentSpellBlockMod', 'FlatEXPBonus', 'PercentEXPBonus', 'FlatEnergyRegenMod', 'FlatEnergyPoolMod', 'PercentLifeStealMod', 
'PercentSpellVampMod']
"""

tank_stats = ['FlatHPPoolMod','PercentHPPoolMod','FlatHPRegenMod','PercentHPRegenMod','FlatArmorMod','PercentArmorMod','FlatBlockMod','PercentBlockMod','FlatSpellBlockMod'
              ,'PercentSpellBlockMod']
fighter_stats = ['FlatPhysicalDamageMod','PercentPhysicalDamageMod','FlatEnergyRegenMod','FlatEnergyPoolMod']
enchanter_stats = ['FlatMovementSpeedMod','PercentMovementSpeedMod','FlatEXPBonus','PercentEXPBonus']
mage_stats = ['FlatMPRegenMod','FlatMPPoolMod','PercentMPPoolMod','PercentMPRegenMod','FlatMagicDamageMod','PercentMagicDamageMod','PercentSpellVampMod']
assassin_stats = ['FlatPhysicalDamageMod','PercentPhysicalDamageMod']
marksman_stats = ['FlatPhysicalDamageMod','PercentPhysicalDamageMod','FlatAttackSpeedMod','PercentAttackSpeedMod','FlatCritChanceMod','FlatCritDamageMod',
                  'PercentCritDamageMod','PercentLifeStealMod']

all_items = json.loads(json.dumps(full_item_data["data"]))

boots = all_items['1001']

#--- I have to import jmespath it's needed for searching in the json, becase riot puts the items in a nested json object, inside a nested object. I can't "slice" the dict

#test just getting the names with the search() function of jmespath
item_names = jmespath.search("*.name",all_items)

#Now let's build a structure like:
"""
Item id (the number that holds the info) | int
Item Name | str
plaintext (description) | str
from (array of item ids, which the item builds from) | List
into (array of item ids, which the item builds into) | List
gold (it's a nested json dict, i'm interested in the "base", "total" and "sell" keys and their values) | nested dict
    -base | int
    -total | int
    -base | int
tags (interesting info, similar to stats, can be used for grouping) | List
stats (most important nested dict, has the info of the stats that the item gives)
    -"stat" | str
"""
#ids = jmespath.search("data.keys(@)",full_item_data) #https://stackoverflow.com/questions/65922565/getting-first-level-with-jmespath
ids = jmespath.search("@.keys(@)",all_items) #both work

print(len(ids))

#we have 573 records
"""
Items with id 7000+ are Ornn items (they have "requiredAlly": "Ornn")
Items with id 443000+ are Arena items (prismatic i think) | "maps": {"11": false,"12": false,"21": false, "22": false,"30": true}
Items with id 220000+ are Normal Arena items
"""

#I will remove ornn items and arena items

#SR_Items = jmespath.search("* | [?requiredAlly!='Ornn']",all_items) #excluding Ornn items and Arena items (Works, but i lose the IDs of the items)
#sr_items_2 = jmespath.search("@[?@.keys(@)=='446693']",all_items)

#sr_items_2 = jmespath.search("@ | [?@=='1001']",all_items) #???? why it doesn't work
#sr_items_2 = jmespath.search("@[?@=='1001']",all_items) #???? why it doesn't work
#Ornn_items = jmespath.search("* | [?requiredAlly=='Ornn']",all_items) #The issue using * on a dict is that you are loosing the keys of it

"""
THERE IS NO ID OF THE OBJECT:

{'name': "The Baron's Gift", 'description': '<mainText><stats><ornnBonus>120</ornnBonus> Ability Power<br><ornnBonus>60%</ornnBonus> Attack Speed<br><ornnBonus>20</ornnBonus>
Ability Haste</stats><br><br><passive>Icathian Bite</passive><br>Attacks apply <magicDamage>magic damage</magicDamage> <OnHit>On-Hit</OnHit>.</mainText>', 'colloq': '', 
'plaintext': '', 'from': ['3115'], 'inStore': False, 'requiredAlly': 'Ornn', 'image': {'full': '7042.png', 'sprite': 'item5.png', 'group': 'item', 
'x': 432, 'y': 288, 'w': 48, 'h': 48}, 'gold': {'base': 0, 'purchasable': False, 'total': 3000, 'sell': 2100}, 'tags': ['AttackSpeed', 'SpellDamage', 'OnHit', 'AbilityHaste'],
'maps': {'11': True, '12': True, '21': True, '22': False, '30': False}, 'stats': {'FlatMagicDamageMod': 120, 'PercentAttackSpeedMod': 0.6}, 'depth': 4}]
"""

#Ornn_items = jmespath.search("[?@.requiredAlly=='Ornn']",all_items)
#Ornn_items = jmespath.search("@.data.[?requiredAlly=='Ornn]",full_item_data)
#Ornn_items = jmespath.search("[{key1:keys(@)[0],a:*.a| [0]},{key1:keys(@)[1],a:*.a| [1]}]",all_items)
#Ornn_items = jmespath.search("[{id:keys(@)},*]",all_items)
#multi-select-hash = "{" ( keyval-expr *( "," keyval-expr ) ) "}"
#keyval-expr       = identifier ":" expression

#all_items.pop("446693") we can delete the data with normal pop() from dict function

keys_deleted = []

#this removes prismatic arena items
for k, v in list(all_items.items()):
    if int(k) > 440000:
        keys_deleted.append(k)
        del all_items[k]
        
len(all_items) #537

#this removes Ornn items
for k, v in list(all_items.items()):
    if int(k) >= 7000 and int(k) < 8000:
        keys_deleted.append(k)
        del all_items[k]
        

len(all_items) #493

#this removes normal arena items
for k, v in list(all_items.items()):
    if int(k) >= 220000 and int(k) < 228021:
        keys_deleted.append(k)
        del all_items[k]

print(keys_deleted)

len(all_items) #309



#let's write it to a file for future use:

with open('items_noArena_NoOrnn(only item data).json', 'w', encoding='utf-8') as f:
    json.dump(all_items, f, ensure_ascii=False, indent=4)


#then let's normalize and make pandas df

items_df = pd.DataFrame(all_items.items(), columns=["ItemID","Data"]) #we take the ItemID (first level) and the Data (Second level) of the dict

#items_df.set_index("ItemID", inplace=True)

items_df = items_df.join(pd.json_normalize(items_df["Data"],max_level=0)) #now we normalize the "Data" column, to unfold the list of dicts, into individual columns | We need to use join to keep the ItemsID column and only normalize Data

items_df = items_df.drop("Data", axis=1) #dropping unnecessary column (Data is the previous nested column)

#Based on the structure mentioned before:
"""
Item id (the number that holds the info) | int
Item Name | str
plaintext (description) | str
from (array of item ids, which the item builds from) | List
into (array of item ids, which the item builds into) | List
gold (it's a nested json dict, i'm interested in the "base", "total" and "sell" keys and their values) | nested dict
    -base | int
    -total | int
    -base | int
tags (interesting info, similar to stats, can be used for grouping) | List
stats (most important nested dict, has the info of the stats that the item gives)
    -"stat" | str
"""

#We create the new df, with only those columns:

items_df.to_csv("items_df.csv") #exporting csv for future use

new_items_df = items_df[["ItemID","name","description","into","gold","tags","stats","from"]]

#before I decided to normalize the JSON with level 0, otherwise we get so many columns for each individual stat

"""
Index(['ItemID', 'name', 'description', 'colloq', 'plaintext', 'into', 'tags',
       'gold.sell', 'maps.11', 'maps.12', 'maps.21', 'maps.22', 'maps.30',
       'stats.FlatMovementSpeedMod', 'from', 'depth', 'stats.FlatHPPoolMod',
       'stats.FlatCritChanceMod', 'stats.FlatMagicDamageMod',
       'stats.FlatMPPoolMod', 'stats.FlatArmorMod', 'stats.FlatSpellBlockMod',
       'inStore', 'effect.Effect1Amount', 'effect.Effect2Amount',
       'effect.Effect3Amount', 'effect.Effect4Amount',
       'stats.FlatPhysicalDamageMod', 'stats.PercentAttackSpeedMod',
       'stats.PercentLifeStealMod', 'stats.FlatHPRegenMod', 'consumed',
       'requiredAlly', 'effect.Effect5Amount', 'effect.Effect6Amount',
       'effect.Effect7Amount', 'effect.Effect8Amount', 'stacks', 'hideFromAll',
       'consumeOnFull', 'stats.PercentMovementSpeedMod', 'specialRecipe',
       'effect.Effect9Amount', 'effect.Effect10Amount',
       'effect.Effect11Amount', 'effect.Effect12Amount',
       'effect.Effect13Amount', 'requiredChampion', 'effect.Effect14Amount',
"""

#for level 0 we get only this

print(items_df.columns)

"""
['ItemID', 'name', 'description', 'colloq', 'plaintext', 'into', 'image',
       'gold', 'tags', 'maps', 'stats', 'from', 'depth', 'inStore', 'effect',
       'consumed', 'requiredAlly', 'stacks', 'hideFromAll', 'consumeOnFull',
       'specialRecipe', 'requiredChampion'],
"""

#and I can access the nested columns later to extract the info 


new_items_df.head()

 
#--------- Give a categorization of what role this item belongs to ( ) ----------#

"""
By this point I noticed the problem was going to be complex. I either df.explode() the "stats" column and give role categorization to individual duplicated rows
And then combine then into 1 group (Role group)

df_exploded = new_items_df.explode("stats")

Or I perform a IsIn or Contains into the "stats" column to see if it contains any stat of the mentioned stat groups of before:

tank_stats = ['FlatHPPoolMod','PercentHPPoolMod','FlatHPRegenMod','PercentHPRegenMod','FlatArmorMod','PercentArmorMod','FlatBlockMod','PercentBlockMod','FlatSpellBlockMod'
              ,'PercentSpellBlockMod']
fighter_stats = ['FlatPhysicalDamageMod','PercentPhysicalDamageMod','FlatEnergyRegenMod','FlatEnergyPoolMod']
enchanter_stats = ['FlatMovementSpeedMod','PercentMovementSpeedMod','FlatEXPBonus','PercentEXPBonus']
mage_stats = ['FlatMPRegenMod','FlatMPPoolMod','PercentMPPoolMod','PercentMPRegenMod','FlatMagicDamageMod','PercentMagicDamageMod','PercentSpellVampMod']
assassin_stats = ['FlatPhysicalDamageMod','PercentPhysicalDamageMod']
marksman_stats = ['FlatPhysicalDamageMod','PercentPhysicalDamageMod','FlatAttackSpeedMod','PercentAttackSpeedMod','FlatCritChanceMod','FlatCritDamageMod',
                  'PercentCritDamageMod','PercentLifeStealMod']

"""
#df.explode() variant
df_exploded = new_items_df.explode("stats")

df_exploded["stats"]

#creating new column in new df
df_exploded["ItemClass"] = ""

#replacing values
#df_exploded.loc[df_exploded['stats'] in tank_stats, 'ItemClass'] = "Tank"

df_exploded["ItemClass"] = df_exploded.where(df_exploded["stats"] in tank_stats, "Tank", df_exploded["ItemClass"])
    
df_exploded.head()

df_exploded.tail()

"""
Gemini recommendation:
"""

# Expand the 'data' column using DataFrame.from_dict
def expand_dict_column(df, col_name):
    # Convert the dictionary column into a DataFrame
    df_expanded = df[col_name].apply(pd.Series)
    # Join with the original DataFrame (assuming necessary columns are present)
    df_final = df.join(df_expanded)
    # Rename columns in the joined DataFrame
    df_final.columns = [*df.columns[:-1], *[f"{col_name}_{x}" for x in df_expanded.columns]]
    return df_final

#df_new = expand_dict_column(df_gemi.copy().rename(columns={'stats': 'temp_stats'}), 'temp_stats')

# Did it outside the function, because I was getting an error
df_gemi = new_items_df.copy()
df_expanded = df_gemi["stats"].apply(pd.Series).fillna('')
df_final = df_gemi.join(df_expanded)
df_final.columns = [*df_gemi.columns, *[f"stats_{x}" for x in df_expanded.columns]]
# why it worked now? I think it was because of the fillna('') that I added

# List of all possible 'stats' keys
all_stats = ['FlatHPPoolMod', 'FlatMPPoolMod', 'PercentHPPoolMod', 'PercentMPPoolMod', 'FlatHPRegenMod', 'PercentHPRegenMod', 'FlatMPRegenMod', 'PercentMPRegenMod', 'FlatArmorMod', 
'PercentArmorMod', 'FlatPhysicalDamageMod', 'PercentPhysicalDamageMod', 'FlatMagicDamageMod', 'PercentMagicDamageMod', 'FlatMovementSpeedMod', 'PercentMovementSpeedMod', 
'FlatAttackSpeedMod', 'PercentAttackSpeedMod', 'PercentDodgeMod', 'FlatCritChanceMod', 'PercentCritChanceMod', 'FlatCritDamageMod', 'PercentCritDamageMod', 'FlatBlockMod',
'PercentBlockMod', 'FlatSpellBlockMod', 'PercentSpellBlockMod', 'FlatEXPBonus', 'PercentEXPBonus', 'FlatEnergyRegenMod', 'FlatEnergyPoolMod', 'PercentLifeStealMod', 
'PercentSpellVampMod']

# Create a DataFrame with all possible 'stats' keys as columns
df_expanded = pd.DataFrame(columns=all_stats)

# Fill in the values from the 'stats' column
for i, stats in df_gemi['stats'].items():
    for key, value in stats.items():
        df_expanded.loc[i, key] = value

# Fill NaN values with ''
df_expanded = df_expanded.fillna('')

# Join the expanded 'stats' DataFrame back to the original DataFrame
df_final = df_gemi.join(df_expanded)

# Fill NaN values with ''
df_final = df_final.fillna('')

# Rename the columns
df_final.columns = [*df_gemi.columns, *[f"stats_{x}" for x in df_expanded.columns]]

"""
last part
"""

# Define the stats categories
tank_stats = ['FlatHPPoolMod','PercentHPPoolMod','FlatHPRegenMod','PercentHPRegenMod','FlatArmorMod','PercentArmorMod','FlatBlockMod','PercentBlockMod','FlatSpellBlockMod'
              ,'PercentSpellBlockMod']
fighter_stats = ['FlatPhysicalDamageMod','PercentPhysicalDamageMod','FlatEnergyRegenMod','FlatEnergyPoolMod']
enchanter_stats = ['FlatMovementSpeedMod','PercentMovementSpeedMod','FlatEXPBonus','PercentEXPBonus']
mage_stats = ['FlatMPRegenMod','FlatMPPoolMod','PercentMPPoolMod','PercentMPRegenMod','FlatMagicDamageMod','PercentMagicDamageMod','PercentSpellVampMod']
assassin_stats = ['FlatPhysicalDamageMod','PercentPhysicalDamageMod']
marksman_stats = ['FlatPhysicalDamageMod','PercentPhysicalDamageMod','FlatAttackSpeedMod','PercentAttackSpeedMod','FlatCritChanceMod','FlatCritDamageMod',
                  'PercentCritDamageMod','PercentLifeStealMod']

# Define the stats categories
stats_categories = {
    'Tank': tank_stats,
    'Fighter': fighter_stats,
    'Enchanter': enchanter_stats,
    'Mage': mage_stats,
    'Assassin': assassin_stats,
    'Marksman': marksman_stats
}

# Function to determine the role based on the stats
def determine_role(row):
    for role, stats in stats_categories.items():
        if any(row[f'stats_{stat}'] != '' for stat in stats):
            return role
    return ''

# Apply the function to each row to create the 'Rol' column
df_final['Rol'] = df_final.apply(determine_role, axis=1)

#drop rows with empty roles (items that don't belong to any category)

df_reduced = df_final.where(df_final["Rol"] != "", inplace=False).dropna()

##--- Determine the amount of cs required to get the gold for the item ---##

#this is a bit more complex, because we need to get the gold value of the item, and then calculate the amount of minions needed to get that gold
#to do so, we need to get the average gold per wave, and then calculate the amount of waves needed to get the gold
#then we can calculate the amount of minions needed to get the gold

# Define the average gold per minion wave
avg_gold_per_wave = 125

# Function to calculate the amount of cs required to get the gold for an item
def calculate_cs_required(row):
    # Get the gold value of the item
    item_gold_value = row['gold']['total'] if 'total' in row['gold'] else 0

    # Calculate the amount of waves needed to get the gold
    waves_required = item_gold_value / avg_gold_per_wave

    # Calculate the amount of minions needed to get the gold
    # Assuming each wave has 6 minions
    cs_required = waves_required * 6

    return round(cs_required)

# Apply the function to each row to create the 'cs_required' column
df_final['cs_required'] = df_final.apply(calculate_cs_required, axis=1)

##--- What game time does this occur at? ---##

# Define the time per minion wave in seconds
time_per_wave = 30

# Function to calculate the amount of waves required to get the gold for the item
def calculate_waves_required(row):
    # Get the gold value of the item
    item_gold_value = row['gold']['total'] if 'total' in row['gold'] else 0

    # Calculate the amount of waves needed to get the gold
    waves_required = item_gold_value / avg_gold_per_wave

    return round(waves_required)

# Apply the function to each row to create the 'waves_required' column
df_final['waves_required'] = df_final.apply(calculate_waves_required, axis=1)

# Define the average gold per minion
avg_gold_per_minion = 25

# Define the time per minion wave in seconds
time_per_wave = 30

# Function to calculate the game time when a player has enough gold to buy an item
def calculate_game_time(row):
    # Get the gold value of the item
    item_gold_value = row['gold']['total'] if 'total' in row['gold'] else 0

    # Calculate the amount of minions needed to get the gold
    minions_required = item_gold_value / avg_gold_per_minion

    # Calculate the amount of waves needed to get the item
    waves_required = item_gold_value / avg_gold_per_wave

    # Calculate the game time in seconds
    game_time = waves_required * time_per_wave

    # Convert the game time to minutes and seconds
    game_time_minutes = game_time // 60
    game_time_seconds = game_time % 60

    return f'{int(game_time_minutes)}:{int(game_time_seconds):02}'

# Apply the function to each row to create the 'game_time' column
df_final['game_time'] = df_final.apply(calculate_game_time, axis=1)

#I didn't add 1:30 to the in-game timer to account for the moment that minions spawn, and also when they reach lane

df_final.to_csv("df_final.csv", index=False)

# i didn`t do the bonus task, because it was too complex and I didn't have the time to do it