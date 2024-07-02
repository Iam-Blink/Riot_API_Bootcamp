import pandas as pd
import json 

champ_data = pd.json_normalize(pd.read_json("champion.json").data)

#we only want the columns "id, key, tags, (stats.attackrange)"

champ_data = champ_data[["id", "key", "tags", "stats.attackrange"]]

champ_data.head()

"""
>>> champ_data.head()
        id  key                  tags  stats.attackrange
0   Aatrox  266             [Fighter]                175
1     Ahri  103      [Mage, Assassin]                550
2    Akali   84            [Assassin]                125
3   Akshan  166  [Marksman, Assassin]                500
4  Alistar   12       [Tank, Support]                125
"""

#we separate the "tags" column into two: "Primary Role" and "Secondary Role", since we are getting 2 items in the list most of the times, sometimes 1

champ_data[["Primary Role", "Secondary Role"]] = champ_data["tags"].apply(lambda x: pd.Series(x) if isinstance(x, list) else pd.Series([x, None]))

champ_data.head()

#Now we get only the ADCs

adc_data = champ_data[champ_data["Primary Role"] == "Marksman"]

adc_data.head()

#Order by attack range (descending)

adc_data = adc_data.sort_values(by="stats.attackrange", ascending=False)

adc_data.head()