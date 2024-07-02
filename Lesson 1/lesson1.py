import pandas as pd

file = "EUW1_6942587793.json"

data = pd.read_json(file)

df = pd.DataFrame(data["info"]["participants"])

df.head(16)

