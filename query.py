import pandas as pd

pd.set_option('display.unicode.east_asian_width', True)
df = pd.read_csv("prices.csv")
df = df.sort_values("価格")
df.to_csv("out.csv")