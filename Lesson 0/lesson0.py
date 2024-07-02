import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

data_file = "GGQXCXCxSHy0AKg9alP1_raw_data.json"

data = pd.read_json(data_file)

df = pd.DataFrame(data)

df.head(5)

#adding a new column to the df

new_df = df.assign(test_column = np.random.randint(1,100,df.shape[0]))
new_df.head(5)

#or
new_df1 = df
new_df1["c"] = ""
new_df1["c"] = np.nan
#or
new_df1["c"] = np.random.randint(1,100,new_df1.shape[0])

new_df1.head(5)


#creating a graph (total damage dealt by game - Renekton)

renekton_data = df.loc[df["champion"] == "Renekton"]
#matches_renek = renekton_data["MatchID"].unique()  #not needed, since all are unique matches

renekton_data.plot(x="MatchID",y="total_damage",kind="bar")

plt.tight_layout()

plt.show()

"""
Solution from course:
"""

df = pd.DataFrame(data)

plt.scatter(df["gold_earned"],df["total_damage"])
plt.xlabel("gold_earned")
plt.ylabel("total_damage")

plt.show()
