import spacy
import pandas as pd
import numpy as np
import re
import rapidfuzz

nlp = spacy.blank("en")
e_nlp = spacy.blank("en")

ruler = nlp.add_pipe("entity_ruler")
e_ruler = e_nlp.add_pipe("entity_ruler")

patterns = pd.read_csv("input_files/patterns.csv").to_dict("records")
ruler.add_patterns(patterns)

e_patterns = pd.read_csv("input_files/extra_patterns.csv")
e_patterns["label"] = e_patterns["label"].apply(str)
e_ruler.add_patterns(e_patterns.to_dict("records"))

def find_extra_pattern(model, gen):
    text = (model + gen)
    doc = e_nlp(text)
    for ent in doc.ents:
        return(ent.label_)

def get_extra_pattern(doc):
    model = ""
    matches = ["air", "mini", "pro", "i3", "i5", "i7"]
    for ent in doc.ents:
        if ent.text in matches:
            model = ent.text
        if (ent.label_ == "gen"):
            gen = ent.text
    pattern = find_extra_pattern(model, gen)
    return (pattern)

def print_stuff(p_str, match, to_print):
    if to_print:
        print(p_str)
        print(match)

def fuzzy_search(product, product_csv):
    to_print = 0
    text = product[1]
    text = text.lower().replace("(", " ").replace(")", " ").replace("[", " ").replace("]", " ")
    text = re.sub("gb\+([1-9])", r"gb + \1", text)
    if to_print:
        print("Text: " + text)
    doc = nlp(text)

    text = product[2]
    text = text.lower().replace("(", " ").replace(")", " ").replace("[", " ").replace("]", " ")
    text = re.sub("gb\+([1-9])", r"gb + \1", text)
    if to_print:
        print("Text: " + text)
    doc2 = nlp(text) if len(text) else None

    brand_len = 0
    total_matches = []
    is_extra = any([token in ["ipad", "i3", "i5", "i7"] for token in text.split()])

    for ent in doc.ents:
        if ent.label_ == "brand" and brand_len == 0:
            for product in product_csv:
                if rapidfuzz.fuzz.partial_token_ratio(ent.text, product[4]) >= 100:
                    total_matches.append(product)
            brand_len = len(total_matches)
            # print("Init brand len: " + str(brand_len))

    if doc2:
        for ent in doc2.ents:
            if ent.label_ == "model" or ent.label_ == "gen":
                if len(total_matches) == 0:
                    for product in product_csv:
                        if rapidfuzz.fuzz.partial_token_ratio(ent.text, product[4]) >= 100:
                            total_matches.append(product)
                    brand_len = len(total_matches)
                print_stuff("Token: ", ent.text, to_print)
                matches = []
                for match in total_matches:
                    if rapidfuzz.fuzz.token_set_ratio(ent.text, match[1]) >= 95:
                        print_stuff("Match: ", match, to_print)
                        matches.append(match)
                    elif rapidfuzz.fuzz.token_set_ratio(re.sub("([a-z])([1-9])", r"\1 \2", str(ent.text)), match[1]) >= 95:
                        print_stuff("Match: ", match, to_print)
                        matches.append(match)
                    elif ent.label_ == "gen" and is_extra and get_extra_pattern(doc) in match[1]:
                        print_stuff("Match: ", match, to_print)
                        matches.append(match)

                # print(matches)
                if len(matches) > 0:
                    total_matches = matches
                if len(total_matches) == 1:
                    break
    
    if doc2:
        for ent in doc2.ents:
            # print(ent.text, ent.label_)
            if ent.label_ == "specs":
                matches = []
                for match in total_matches:
                    if ("+" + ent.text) in match[1] or ("(" + ent.text) in match[4] or "(" + ent.text.replace("gb", "") in match[1] or "/" + ent.text in match[1] or ent.text + "/" in match[1] or ent.text.replace("gb", "") + "/" in match[1]:
                        # print(match[1])
                        print_stuff("Match: ", match, to_print)
                        matches.append(match)
                if len(matches) > 0:
                    total_matches = matches
                if len(total_matches) == 1:
                    break

    if len(total_matches) > 1:
        for ent in doc.ents:
            if ent.label_ == "model" or ent.label_ == "gen":
                if len(total_matches) == 0:
                    for product in product_csv:
                        if rapidfuzz.fuzz.partial_token_ratio(ent.text, product[4]) >= 100:
                            total_matches.append(product)
                    brand_len = len(total_matches)
                print_stuff("Token: ", ent.text, to_print)
                matches = []
                for match in total_matches:
                    if rapidfuzz.fuzz.token_set_ratio(ent.text, match[1]) >= 95:
                        print_stuff("Match: ", match, to_print)
                        matches.append(match)
                    elif rapidfuzz.fuzz.token_set_ratio(re.sub("([a-z])([1-9])", r"\1 \2", str(ent.text)), match[1]) >= 95:
                        print_stuff("Match: ", match, to_print)
                        matches.append(match)
                    elif ent.label_ == "gen" and is_extra and get_extra_pattern(doc) in match[1]:
                        print_stuff("Match: ", match, to_print)
                        matches.append(match)

                # print(matches)
                if len(matches) > 0:
                    total_matches = matches
                if len(total_matches) == 1:
                    break

    if len(total_matches) > 1:
        for ent in doc.ents:
            # print(ent.text, ent.label_)
            if ent.label_ == "specs":
                matches = []
                for match in total_matches:
                    if ("+" + ent.text) in match[1] or ("(" + ent.text) in match[4] or "(" + ent.text.replace("gb", "") in match[1] or "/" + ent.text in match[1] or ent.text + "/" in match[1] or ent.text.replace("gb", "") + "/" in match[1]:
                        # print(match[1])
                        print_stuff("Match: ", match, to_print)
                        matches.append(match)
                if len(matches) > 0:
                    total_matches = matches
                if len(total_matches) == 1:
                    break

    if len(total_matches) > 1:
        for ent in doc.ents:
            if ent.label_ == "year":
                matches = []
                for match in total_matches:
                    if ent.text in match[4]:
                        print_stuff("Match: ", match, to_print)
                        matches.append(match)
                if len(matches) > 0:
                    total_matches = matches
                if len(total_matches) == 1:
                    break

    if len(total_matches) > 1:
        for ent in doc.ents:
            if ent.label_ == "network":
                matches = []
                for match in total_matches:
                    if ent.text in match[4]:
                        print_stuff("Match: ", match, to_print)
                        matches.append(match)
                total_matches = matches
                if len(total_matches) == 1:
                    break

    if to_print:
        print("Total matches: ")
        for match in total_matches:
            print(match)
        print("\n")

    # print("End brand len: " + str(brand_len))
    # print("Total len: " + str(len(total_matches)))

    return (min([list(match) for match in total_matches], key = lambda m: m[2]) if len(total_matches) and len(total_matches) != brand_len else "Not found")

# data_csv = pd.read_csv("exported_products_27_18_13_32_expected.csv")
# data = data_csv.to_numpy()

product_csv = pd.read_csv("input_files/products.csv")
product_csv["PSmodelNameLower"] = product_csv["PSmodelName"].str.lower()
product_csv = product_csv.to_numpy()

# print(fuzzy_search("REDMI NOTE 10 PRO(8GB+128GB) [ORIGINAL XIAOMI MALAYSIA] * (READY STOCK) XIAOMI REDMI", 0))

# print(fuzzy_search("Apple 11-inch iPad Pro 3rd Gen,Wi-Fi + Cellular", 1))

# for product in data:
#     print(fuzzy_search(str(product[1]), 0))
# print("NEWLINE HERE \n")
# for product in data:
#     print(product[2])

# print("Accuracy: " + str(sum([fuzzy_search(str(product[1]), 0) == product[2] for product in data]) / len(data) * 100) + "%")

df = pd.read_json("input_files/lazada.json")
# joined_df = pd.merge(df, data_csv[["productURL", "PSproductKey"]], on = "productURL", how = "left")
arr_df = df.to_numpy()
output = [fuzzy_search(product, product_csv) for product in arr_df]

df["PSproductKey"] = [o[2] if type(o) == list else o for o in output]
df["PSmodelName"] = [o[1] if type(o) == list else o for o in output]
df["Category"] = [o[3] if type(o) == list else o for o in output]
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
df.to_csv("output.csv", index = False)
# print("Accuracy: " + str(sum([fuzzy_search(str(product[1]), 0) == product[5] for product in df_arr]) / len(df_arr) * 100) + "%")