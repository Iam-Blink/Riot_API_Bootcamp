import pandas as pd

file = "lol-match-v5 match data example.json"

data = pd.read_json(file)

df = pd.DataFrame(data["info"]["participants"])

df.head(16)

df_participant1 = pd.DataFrame(data["info"]["participants"][0])

df_participant1.head()