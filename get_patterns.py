import pandas as pd
import re

def format_model(model, brands):
    model = model.lower()
    for brand in brands.str.lower().unique():
        model = model.replace(brand, "")
    model = model.strip().replace("[", " ").replace("]", " ").replace(",", " ").replace("\"", "")
    return (re.sub("\(.*?\)", "", model))

df = pd.read_csv("input_files/products.csv", header = None, skiprows = [0])
patterns = []
excludes = ["gb", "gen", "wi-fi", "cellular"]
years = [str(year) for year in range(2017, 2023)]
unique_tokens = set()

for brand in df[0].str.lower().unique():
    patterns.append({"label": "brand", "pattern": brand})

df[1] = df[1].apply(format_model, brands = df[0])
for model in df[1].unique():
    tokens = model.split()
    for i, token in enumerate(tokens):
        if len(token) > 1 and token not in excludes and token not in years and "gb" not in token:
            unique_tokens.add(token)
        if token.isnumeric() and tokens[i - 1].isalpha():
            unique_tokens.add(tokens[i - 1] + token)

for r in range(1, 4):
    patterns.append({"label": "specs", "pattern": str(r) + "gb"})

for r2 in range(4, 17, 2):
    patterns.append({"label": "specs", "pattern": str(r2) + "gb"})

for s in list(map(lambda x: 2 ** x, range(5, 10))):
    patterns.append({"label": "specs", "pattern": str(s) + "gb"})

for s2 in range(1, 3):
    patterns.append({"label": "specs", "pattern": str(s2) + "tb"})

for p in range(3, 10, 2):
    patterns.append({"label": "specs", "pattern": "i" + str(p)})

patterns.append({"label": "network", "pattern": "wi-fi"})
patterns.append({"label": "network", "pattern": "cellular"})

for y in years:
    patterns.append({"label": "year", "pattern": y})

for token in unique_tokens:
    patterns.append({"label": "model", "pattern": token})

for g in range(3, 16):
    if (g > 3):
        patterns.append({"label": "gen", "pattern": str(g) + "th"})
    else:
        patterns.append({"label": "gen", "pattern": str(g) + "rd"})

patterns_df = pd.DataFrame(patterns)
patterns_df.to_csv("input_files/patterns.csv", index = False)